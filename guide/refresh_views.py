"""Refresh the guide and extended notes from the canonical standalone catalogue.

Usage: python3 refresh_views.py
No external packages, bibliography engine, TeX includes or network required.
Edit route choices/rationales in learning_routes.json; bibliographic text lives
only in institutional_quantitative_finance_reading_list.tex.
"""
from pathlib import Path
import html, json, re, textwrap, unicodedata
from datetime import date

ROOT = Path(__file__).resolve().parent
CATALOGUE = 'institutional_quantitative_finance_reading_list'
GUIDE = 'institutional_quantitative_finance_learning_guide'

PART_WORDS=['zero','one','two','three','four','five','six','seven','eight','nine','ten']
def argument(s, i):
    while s[i].isspace(): i += 1
    assert s[i]=='{',s[i:i+100]
    depth=1; j=i+1
    while j<len(s):
        if s[j]=='\\':j+=2;continue
        if s[j]=='{':depth+=1
        if s[j]=='}':depth-=1
        if depth==0:return s[i+1:j],j+1
        j+=1
    raise ValueError('Unbalanced argument at '+str(i))

def commands(source, name, count):
    result=[]
    for m in re.finditer(r'^\\'+name+r'\{',source,re.M):
        args=[];i=m.end()-1
        for _ in range(count):
            a,i=argument(source,i);args.append(a)
        result.append(args)
    return result

def unlinked(s):
    """Keep TeX typography; strip nested destinations from a linked guide title."""
    out='';i=0
    while i<len(s):
        m=re.match(r'\\(href|hyperlink|hypertarget)\{',s[i:])
        if m:
            a,j=argument(s,i+m.end()-1); b,k=argument(s,j)
            out+= '' if m[1]=='hypertarget' else unlinked(b);i=k
        elif s.startswith('\\sourcecite{',i):
            _,i=argument(s,i+len('\\sourcecite'))
        else:out+=s[i];i+=1
    return out

def tex_escape(s):
    return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}.get(c,c) for c in s)

def validate_pathway(data):
    """Keep editorial placement, prerequisite links and stable route identities aligned."""
    routes=data['routes']; specialists=data['specialist_routes']
    overviews={r['id']:r for r in routes}
    all_routes={r['id']:r for r in routes+specialists}
    assert len(all_routes)==len(routes)+len(specialists),'Duplicate pathway identifiers'
    for identifier in all_routes:
        assert re.fullmatch(r'[a-z0-9-]+',identifier),identifier
    parts=data['learning_parts']
    assert len({p['id'] for p in parts})==len(parts),'Duplicate part identifiers'
    ordered=[identifier for part in parts for identifier in part['routes']]
    assert len(ordered)==len(set(ordered)) and set(ordered)==set(overviews),'Overview placement mismatch'
    children=[identifier for r in routes for identifier in r['specialist_order']]
    assert len(children)==len(set(children)) and set(children)=={r['id'] for r in specialists},'Specialist placement mismatch'
    sequence=[]
    for identifier in ordered:
        sequence.extend([identifier]+overviews[identifier]['specialist_order'])
    positions={identifier:n for n,identifier in enumerate(sequence)}
    for r in all_routes.values():
        for prerequisite in r.get('prerequisite_routes',[]):
            assert prerequisite in all_routes,(r['id'],prerequisite)
            assert positions[prerequisite]<positions[r['id']],('Prerequisite must precede pathway',r['id'],prerequisite)
    legacy=[r['legacy_label'] for r in routes]
    assert len(legacy)==len(set(legacy)),'Duplicate legacy route labels'
    # An overview's outcome is what its checkpoint tests; its section goals map the wider
    # coverage to the pathways that teach it, and a capstone checkpoint names those it needs.
    for r in routes:
        members=set(r['specialist_order'])
        goals=r.get('section_goals',[])
        assert goals and all(g['goal'] and g['pathways'] for g in goals),('Overview needs section goals',r['id'])
        taught={p for g in goals for p in g['pathways']}
        assert taught==members,('Section goals must map every pathway in the section and no other',r['id'],sorted(taught^members))
        assert set(r.get('checkpoint_after',[]))<=members,('A capstone checkpoint follows pathways in its own section',r['id'])
    for r in specialists:
        assert 'section_goals' not in r and 'checkpoint_after' not in r,('Only overviews have section goals or capstones',r['id'])
    return overviews,all_routes

def one_line_commands(source):
    """Keep each catalogue command on one line, so that a line diff of the catalogue finds every changed entry."""
    for m in re.finditer(r'^\\(CatalogueEntry|ExtendedNote|EntryRecency)\{',source,re.M):
        i=m.end()-1
        for _ in range(2 if m[1]=='ExtendedNote' else 7):_,i=argument(source,i)
        assert '\n' not in source[m.start():i] and source[i:i+1] in ('\n',''),('Keep each catalogue command on one line',source[m.start():m.start()+80])

def number_link(identifier, all_routes):
    label=('route-' if 'legacy_label' in all_routes[identifier] else 'specialist-')+identifier
    return r'\hyperref['+label+r']{\ref*{'+label+'}}'

def and_list(items):
    return items[0] if len(items)==1 else ', '.join(items[:-1])+' and '+items[-1]

def route_link(identifier, all_routes, text=None):
    r=all_routes[identifier]
    label=('route-' if 'legacy_label' in r else 'specialist-')+identifier
    return r'\hyperref['+label+']{'+tex_escape(text or r['name'])+'}'

def chart_node(identifier, all_routes, x, y, width='2.85cm', style='pathnode', show_count=False):
    r=all_routes[identifier]
    label=('route-' if 'legacy_label' in r else 'specialist-')+identifier
    title=r'\textbf{\ref*{'+label+r'}.} '+tex_escape(r.get('chart_name',r['name']))
    if show_count:
        title+=r'\\[2pt]{\small '+str(len(r['specialist_order']))+' pathways}'
    # Measure the actual wrapped label in TeX; the whole interior stays clickable.
    # Long refreshed titles grow their boxes instead of overflowing a fixed parbox.
    content=r'\MeasurePathNode{'+width+'}{'+title+'}'
    content+=r'\hyperref['+label+r']{\parbox[c][\pathnodeheight][c]{'+width+r'}{\centering '+title+'}}'
    return r'\node['+style+'] ('+identifier+') at ('+str(x)+','+str(y)+') {'+content+'};\n'

def overview_chart(parts, all_routes):
    """Whole-guide DAG: one row per part, or per group in a part's `chart_rows`.

    A dashed spine from the first foundation section, the shared prerequisite of every
    subject part, feeds each later row. Solid arrows give the recommended study order
    within a row; they are not hard gates. Rows hold at most four sections. The page
    holds only the heading and the chart, which "Using the routes" explains, so that
    the chart is never split from its heading.
    """
    cols=4;step=4.15;width='3.30cm';spine=-2.40;label_x=-1.80
    roman=['I','II','III','IV','V','VI','VII','VIII','IX','X']
    result=[r'''\clearpage
\section*{Learning pathway DAG}\phantomsection\label{learning-map}
\markboth{Learning pathway DAG}{}
\addcontentsline{toc}{section}{Learning pathway DAG}
\begin{center}
\begin{tikzpicture}[x=1cm,y=1cm]
''']
    y=0;rows=[]
    for i,part in enumerate(parts):
        groups=part.get('chart_rows') or [part['routes'][k:k+cols] for k in range(0,len(part['routes']),cols)]
        assert [m for g in groups for m in g]==part['routes'],('chart_rows must list the part sections in order',part['id'])
        assert max(len(g) for g in groups)<=cols,('Whole-guide DAG row is wider than four sections',part['id'])
        label=r'\hyperref[part-'+part['id']+']{PART '+roman[i]+': '+tex_escape(part['title']).upper()+'}'
        result.append(r'\node[maplabel,anchor=west] at ('+f'{label_x:.2f},{y:.2f}'+') {'+label+'};\n')
        y-=1.10
        for j,group in enumerate(groups):
            if j:y-=1.80
            for k,identifier in enumerate(group):
                result.append(chart_node(identifier,all_routes,f'{k*step:.2f}',f'{y:.2f}',width=width,show_count=True))
            for a,b in zip(group,group[1:]):
                result.append(r'\draw[patharrow] ('+a+'.east) -- ('+b+'.west);\n')
            rows.append((y,group))
        y-=1.25
    source=parts[0]['routes'][0]
    result.append(r'\draw[entryline] ('+source+'.west) -- ('+f'{spine:.2f},{rows[0][0]:.2f}'+') -- ('+f'{spine:.2f},{rows[-1][0]:.2f}'+');\n')
    for row_y,group in rows:
        if source not in group:
            result.append(r'\draw[entryarrow] ('+f'{spine:.2f},{row_y:.2f}'+') -- ('+group[0]+'.west);\n')
    result.append('\\end{tikzpicture}\n\\end{center}\n')
    return ''.join(result)

def section_dag_label(identifier):
    return 'digital-map' if identifier=='digital-assets-prediction-markets' else 'map-'+identifier

def spread(desired, step, lo, hi):
    """Keep nodes in their given order, at least `step` apart within [lo, hi], near `desired`."""
    xs=[]
    for d in desired:xs.append(max(d,xs[-1]+step) if xs else max(d,lo))
    for i in range(len(xs)-1,-1,-1):xs[i]=min(xs[i],hi if i==len(xs)-1 else xs[i+1]-step)
    # Centre a crowded group on its targets without leaving the chart width.
    shift=sum(d-x for d,x in zip(desired,xs))/len(xs)
    shift=max(lo-xs[0],min(shift,hi-xs[-1]))
    return [x+shift for x in xs]

def section_chart(root_id, overviews, all_routes):
    """Focused DAG for one overview section.

    Entry pathways (no prerequisite inside the section) sit in subsection order on the
    first row, fed by a dashed rail from the overview; pathways with in-section
    prerequisites sit below them, and each parent is centred over its children. When
    more than four pathways are entries, or when the rows cannot centre a parent over
    the pathways that depend only on it, prerequisite trees are packed in subsection
    order into balanced rows, each with its own rail. Solid arrows are in-section
    prerequisites; cross-section prerequisites are listed below the chart.
    """
    root=overviews[root_id]; members=list(root['specialist_order'])
    mset=set(members)
    parents={m:[p for p in all_routes[m].get('prerequisite_routes',[]) if p in mset] for m in members}
    for m in members:
        for p in parents[m]:
            assert members.index(p)<members.index(m),('In-section prerequisite must precede',m,p)
    depth={}
    def d(m):
        if m not in depth:depth[m]=1+max([d(p) for p in parents[m]],default=0)
        return depth[m]
    for m in members:d(m)
    levels={level:[m for m in members if depth[m]==level] for level in sorted(set(depth.values()))}
    cols=4;step=4.15;width='3.65cm';row=2.30;top=-2.75
    pos={};rails=[]
    if max(map(len,levels.values()))<=cols:
        # Layered layout: each deeper pathway starts under the mean of its parents.
        right=(max(map(len,levels.values()))-1)*step
        for level,nodes in levels.items():
            if level==1:
                xs=[i*step for i in range(len(nodes))]
            else:
                target={m:sum(pos[p][0] for p in parents[m])/len(parents[m]) for m in nodes}
                nodes=sorted(nodes,key=target.get)
                xs=spread([target[m] for m in nodes],step,0,right)
            for m,x in zip(nodes,xs):pos[m]=(x,top-(level-1)*row)
        # Then centre each parent over its children, keeping its row order.
        for level in sorted(levels,reverse=True)[1:]:
            nodes=sorted(levels[level],key=lambda m:pos[m][0])
            target=[]
            for m in nodes:
                below=[c for c in levels.get(level+1,[]) if m in parents[c]]
                target.append(sum(pos[c][0] for c in below)/len(below) if below else pos[m][0])
            for m,x in zip(nodes,spread(target,step,0,right)):pos[m]=(x,pos[m][1])
        rails.append((top+row/2,levels[1]))
        # A packed entry row can leave a parent off-centre, so a slanted arrow runs under
        # a neighbouring entry; the tree layout below gives each parent its own columns.
        for m in members:
            only=[c for c in members if parents[c]==[m]]
            if only and abs(pos[m][0]-sum(pos[c][0] for c in only)/len(only))>0.01:
                pos={};rails=[];break
    if not pos:
        # Wrapped layout: a pathway hangs under its latest in-section prerequisite.
        tree_parent={m:max(parents[m],key=members.index) for m in members if parents[m]}
        kids={m:[c for c in members if tree_parent.get(c)==m] for m in members}
        def span(m):return max(1,sum(span(c) for c in kids[m]))
        def height(m):return 1+max([height(c) for c in kids[m]],default=0)
        entries=levels[1]
        total=sum(span(m) for m in entries)
        target=-(-total//-(-total//cols))
        bands=[[]];used=0
        for m in entries:
            assert span(m)<=cols,('Section DAG prerequisite tree is wider than four columns',root_id,m)
            if bands[-1] and used+span(m)>target:bands.append([]);used=0
            bands[-1].append(m);used+=span(m)
        y=top
        def put(m,col,level):
            pos[m]=((col+(span(m)-1)/2)*step,y-level*row)
            for c in kids[m]:put(c,col,level+1);col+=span(c)
        for band in bands:
            col=0
            for m in band:put(m,col,0);col+=span(m)
            rails.append((y+row/2,band))
            y-=max(height(m) for m in band)*row
    # Subsection numbers must read row by row, left to right, through the drawn chart.
    drawn=sorted(members,key=lambda m:(-round(pos[m][1],2),round(pos[m][0],2)))
    assert drawn==members,('Reorder specialist_order to follow the chart row by row',root_id,drawn)
    root_x=max(x for x,_ in pos.values())/2
    left=-2.35
    out=[r"""\clearpage
\subsection*{CHART_TITLE}\phantomsection\label{LABEL}
\addcontentsline{toc}{subsection}{TITLE: pathway DAG}
Start with the section overview's readings, for orientation. Solid arrows show prerequisites within this section. Dashed connectors identify entry points with no further prerequisite in this section; the linked foundations below still apply. Follow the arrows for dependencies and the subsection numbers for reading order. Every node is clickable.
\begin{center}\begin{tikzpicture}[x=1cm,y=1cm]
""".replace('CHART_TITLE',tex_escape(root['name'])+': pathway DAG').replace('TITLE',tex_escape(root['name'])).replace('LABEL',section_dag_label(root_id))]
    out.append(chart_node(root_id,all_routes,f'{root_x:.2f}',0,width='4.6cm'))
    for m in members:
        out.append(chart_node(m,all_routes,f'{pos[m][0]:.2f}',f'{pos[m][1]:.2f}',width=width))
    first_rail=max(r for r,_ in rails)
    last_rail=min(r for r,_ in rails)
    out.append(r'\draw[entryline] ('+root_id+'.south) -- ('+f'{root_x:.2f},{first_rail:.2f}'+');\n')
    if len(rails)>1:
        out.append(r'\draw[entryline] ('+f'{left:.2f},{first_rail:.2f}'+') -- ('+f'{left:.2f},{last_rail:.2f}'+');\n')
    for ry,entries in rails:
        xs=[pos[m][0] for m in entries]
        rail_left=left if len(rails)>1 else min(min(xs),root_x)
        rail_right=max(max(xs),root_x) if ry==first_rail else max(xs)
        out.append(r'\draw[entryline] ('+f'{rail_left:.2f},{ry:.2f}'+') -- ('+f'{rail_right:.2f},{ry:.2f}'+');\n')
        for m in entries:
            out.append(r'\draw[entryarrow] ('+f'{pos[m][0]:.2f},{ry:.2f}'+') -- ('+m+'.north);\n')
    edges=[(p,m) for m in members for p in parents[m]]
    def elbow(p,m):
        """Route a long cross-column arrow down the parent's column, then across the gap
        above the child into its parent-side shoulder. None when a node or arrow is in the way."""
        (px,py),(cx,cy)=pos[p],pos[m]
        if abs(px-cx)<0.01:return None
        gap=cy+row/2;ex=cx+(0.6 if px>cx else -0.6)
        for n,(nx,ny) in pos.items():
            if n not in (p,m) and abs(nx-px)<step/2 and gap<ny<py:return None
        lo,hi=sorted((px,ex))
        for a,b in edges:
            if (a,b)!=(p,m) and pos[a][1]>gap>pos[b][1] and lo<(pos[a][0]+pos[b][0])/2<hi:return None
        return f'{px:.2f},{gap:.2f}',f'{ex:.2f},{gap:.2f}',f'{ex:.2f},0'
    for p,m in edges:
        if abs(pos[p][1]-pos[m][1])>row+0.01:
            route=elbow(p,m)
            if route:
                out.append(r'\draw[patharrow] ('+p+'.south) -- ('+route[0]+') -- ('+route[1]+') -- ('+m+'.north -| '+route[2]+');\n')
            else:
                out.append(r'\draw[patharrow] ('+p+'.south) .. controls +(0,-0.9) and +(0,0.9) .. ('+m+'.north);\n')
        else:
            out.append(r'\draw[patharrow] ('+p+'.south) -- ('+m+'.north);\n')
    out.append(r'\end{tikzpicture}\end{center}'+'\n')
    if root.get('checkpoint_after'):
        out.append(r'\textbf{Overview checkpoint.} A section capstone: complete it after '+and_list([number_link(p,all_routes) for p in root['checkpoint_after']])+'.\n\n')
    external={}
    for m in members:
        for p in all_routes[m].get('prerequisite_routes',[]):
            if p not in mset and p!=root_id:external.setdefault(p,[]).append(m)
    if external:
        out.append(r'\textbf{Bring these foundations with you.}\begin{itemize}'+'\n')
        for p,ms in external.items():
            out.append(r'\item '+route_link(p,all_routes)+' --- needed by '+', '.join(route_link(m,all_routes,all_routes[m].get('chart_name',all_routes[m]['name'])) for m in ms)+'.\n')
        out.append(r'\end{itemize}')
    out.append(r'\hyperref[learning-map]{Return to the whole-guide DAG.}'+'\n')
    return ''.join(out)

def label_destinations():
    p=ROOT/(CATALOGUE+'.aux')
    if not p.exists():return {}
    return {m[1]:m[2] for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{[^}]*\}\{.*?\}\{([^}]+)\}',p.read_text())}

def page_destinations():
    """Read page fallbacks from the catalogue's own TeX auxiliary output."""
    p=ROOT/(CATALOGUE+'.aux')
    if not p.exists():return {}
    pages={}
    for line in p.read_text().splitlines():
        if not line.startswith('\\newlabel{'):continue
        label,j=argument(line,len('\\newlabel'))
        fields,j=argument(line,j)
        try:
            _,j=argument(fields,0);page,j=argument(fields,j)
            _,j=argument(fields,j);dest,j=argument(fields,j)
        except (AssertionError,IndexError,ValueError):continue
        if not page.isdigit():continue
        if label.startswith('entry-'):
            pages[label[len('entry-'):]]=int(page)
        else:
            pages.setdefault(dest,int(page))
    return pages

def web_url(s):
    return s.replace(r'\_','_').replace(r'\%','%').replace(r'\&','&').replace(r'\#','#').replace('~','~')

def to_html(s, labels):
    """Render the small TeX prose subset used by the catalogue, without TeX input."""
    out=[];i=0
    accent={"'":'\u0301','`':'\u0300','"':'\u0308','^':'\u0302','~':'\u0303','c':'\u0327','u':'\u0306','H':'\u030b','v':'\u030c','=':'\u0304'}
    special={'textquotesingle':"'",'textquotedblleft':'“','textquotedblright':'”','textquoteleft':'‘','textquoteright':'’','textendash':'–','textemdash':'—','ss':'ß','O':'Ø','o':'ø','i':'ı','ae':'æ','AA':'Å','LaTeX':'LaTeX','par':'<br>','newline':'<br>','quad':' ','enspace':' ','textasciitilde':'~','textasciicircum':'^'}
    while i<len(s):
        if s[i]=='\\':
            m=re.match(r'\\([A-Za-z]+|.)\s*',s[i:])
            if not m: i+=1;continue
            cmd=m[1];j=i+m.end()
            if cmd in ['&','%','$','#','_','{','}']:
                out.append(html.escape(cmd));i=j;continue
            if cmd in accent and j<len(s):
                if s[j]=='{':a,k=argument(s,j)
                else:a,k=s[j],j+1
                out.append(html.escape(unicodedata.normalize('NFC',a+accent[cmd])));i=k;continue
            if cmd in ['href','hyperlink','hypertarget']:
                a,j=argument(s,j);b,j=argument(s,j)
                if cmd!='hypertarget':
                    url=web_url(a) if cmd=='href' else '#'+a
                    out.append('<a href="'+html.escape(url,quote=True)+'">'+to_html(b,labels)+'</a>')
                i=j;continue
            if cmd=='hyperref' and j<len(s) and s[j]=='[':
                k=s.index(']',j);target=s[j+1:k];a,j=argument(s,k+1)
                out.append('<a href="#'+html.escape(target,quote=True)+'">'+to_html(a,labels)+'</a>');i=j;continue
            if cmd in ['ref','sourcecite']:
                a,j=argument(s,j);dest=a if cmd=='ref' else 'source-'+a
                out.append('<a href="#'+html.escape(dest,quote=True)+'">'+html.escape(a if cmd=='sourcecite' else 'catalogue section')+'</a>');i=j;continue
            if cmd=='url':
                a,j=argument(s,j);url=html.escape(web_url(a),quote=True)
                out.append('<a href="'+url+'">'+url+'</a>');i=j;continue
            if cmd in ['emph','textit','textbf','texttt','mbox','zh','textrm','textnormal','textsuperscript']:
                a,j=argument(s,j);tag={'emph':'em','textit':'em','textbf':'strong','texttt':'code','textsuperscript':'sup'}.get(cmd,'span')
                out.append('<'+tag+'>'+to_html(a,labels)+'</'+tag+'>');i=j;continue
            if cmd in ['label','Needspace']:
                if j<len(s) and s[j]=='{':_,j=argument(s,j)
                i=j;continue
            if cmd in special:out.append(special[cmd]);i=j;continue
            # Remaining mathematical/formatting commands are shown as readable text.
            out.append(html.escape(cmd));i=j;continue
        if s[i] not in '{}$':out.append(html.escape(s[i]))
        i+=1
    return ''.join(out).replace('---','—').replace('--','–').replace('``','“').replace("''",'”')

def refresh():
    source=(ROOT/(CATALOGUE+'.tex')).read_text()
    one_line_commands(source)
    records=commands(source,'CatalogueEntry',7)
    notes=commands(source,'ExtendedNote',2)
    recency_rows=commands(source,'EntryRecency',7)
    recency={r[0]:r[1:] for r in recency_rows}
    by_anchor={r[0]:r for r in records}
    assert len(by_anchor)==len(records),'Duplicate catalogue identifiers'
    assert len(recency)==len(recency_rows),'Duplicate recency identifiers'
    assert set(recency)==set(by_anchor),'Every catalogue entry needs one recency record'
    for r in records:
        for alias in re.findall(r'\\hypertarget\{([^}]+)\}',r[1]):by_anchor[alias]=r
    labels=label_destinations()
    declared_labels=set(re.findall(r'\\label\{([^}]+)\}',source))
    route_data=json.loads((ROOT/'learning_routes.json').read_text())
    as_of=route_data.get('as_of','2026-10-04')
    edition_date=date.fromisoformat(as_of)
    display_date=f'{edition_date.day} {edition_date.strftime("%B %Y")}'
    link_target=route_data.get('catalogue_link_target','pdf')
    assert link_target in ('html','pdf'),'Unknown catalogue link target'
    html_links=link_target=='html'
    routes=route_data['routes']
    specialists=route_data.get('specialist_routes',[])
    overviews,all_routes=validate_pathway(route_data)
    parts=route_data['learning_parts']
    route_labels={r['name']:'route-'+r['id'] for r in routes}
    placement={sid:r['id'] for r in routes for sid in r['specialist_order']}
    specialist_ids=[r['id'] for r in specialists]
    assert len(set(specialist_ids))==len(specialist_ids),'Duplicate specialist route ids'
    for r in specialists:
        assert re.fullmatch(r'[a-z0-9-]+',r['id']),r['id']
        assert r['parent_route'] in route_labels,r['parent_route']
    for r in routes+specialists:
        assert r['required_readings'],r['name']
        assert len({rd['anchor'] for rd in r['required_readings']})==len(r['required_readings']),r['name']
        for reading in r['required_readings']:assert reading['anchor'] in by_anchor,reading
        for b in r['optional_branches']:assert b['target'] in declared_labels or b['target'] in by_anchor,b
    route_summary=f"{len(routes)} overview routes and {len(specialists)} specialist pathways"

    preamble=source[:source.index('\\begin{document}')]
    # Retain the catalogue's 9pt body size for compact guide reading lists.
    preamble=preamble.replace('extreport','extarticle')
    preamble=preamble.replace(r'\fontsize{7}{8}',r'\fontsize{6.3}{7.2}')
    # Report-only chapter settings and catalogue entry declarations are unnecessary.
    preamble=preamble[:preamble.index('\\titleformat{\\chapter}')]
    preamble=preamble.replace('Institutional Quantitative Finance Reference Catalogue','Institutional Quantitative Finance Learning Guide')
    preamble=preamble.replace('Four-part institutional quantitative research reference catalogue',route_summary)
    preamble+=r'''\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\definecolor{pathfill}{HTML}{EDF3F5}
\definecolor{pathrule}{HTML}{7E969F}
% Keep page fallbacks intact and attached to the end of the linked text.
\newcommand{\CataloguePage}[1]{\nobreakspace{\small\mbox{(Catalogue p.\,#1)}}}
\newcommand{\BranchPage}[1]{\nobreakspace\mbox{(p.\,#1)}}
% Note keys (catalogue identifiers and pathway ids) end their line, flush right.
\definecolor{notekey}{HTML}{4F6670}
\newcommand{\NoteKey}[1]{\unskip\nobreak\hfill\penalty50\hskip1em\hbox{}\nobreak\hfill{\fontsize{7.2}{8.6}\selectfont\ttfamily\color{notekey}#1}{\parfillskip=0pt\par}}
\newsavebox{\pathnodebox}
\newlength{\pathnodeheight}
\newcommand{\MeasurePathNode}[2]{%
  \sbox{\pathnodebox}{\parbox{#1}{\centering #2}}%
  \setlength{\pathnodeheight}{\dimexpr\ht\pathnodebox+\dp\pathnodebox\relax}%
  \ifdim\pathnodeheight<1.30cm\setlength{\pathnodeheight}{1.30cm}\fi
}
\tikzset{
 pathnode/.style={draw=pathrule,fill=pathfill,rounded corners=3pt,inner sep=4pt,font=\fontsize{9}{10.35}\selectfont},
 patharrow/.style={-{Stealth[length=2mm]},draw=catalogueink,line width=.7pt},
 pathline/.style={draw=catalogueink,line width=.7pt},
 entryarrow/.style={patharrow,dashed},
 entryline/.style={pathline,dashed},
 maplabel/.style={font=\fontsize{7.2}{9}\selectfont\bfseries,text=catalogueink,fill=white,inner sep=2pt}
}
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{2}
\titleformat{\part}[display]{\centering\color{catalogueink}\bfseries}{\large PART \thepart}{10pt}{\fontsize{21.6}{25.2}\selectfont}
\titleformat{\section}{\fontsize{14.4}{17.1}\selectfont\bfseries\color{catalogueink}}{\thesection}{0.6em}{}
\titleformat{\subsection}{\fontsize{11.7}{14.4}\selectfont\bfseries\color{catalogueink}}{\thesubsection}{0.6em}{}
\setlist[enumerate]{leftmargin=1.8em,itemsep=7pt,topsep=5pt}
'''
    guide=[ '% Generated by refresh_views.py. Edit learning_routes.json and canonical catalogue, then refresh.\n',preamble,
      r'''\begin{document}
\begin{titlepage}\centering\vspace*{3cm}
{\fontsize{21.6}{26.1}\selectfont\bfseries Institutional\\Quantitative Finance\\[8pt]Learning Guide}\par\vspace{1cm}
{\large PART_COUNT_CAP parts: foundations to specialist applications}\par\bigskip
{\large ROUTE_SUMMARY}\par\vfill
EDITION_DATE\par\bigskip
Learning pathway revised PATHWAY_DATE\par\bigskip
Companion to the canonical reference catalogue\par
\end{titlepage}
\setcounter{page}{2}
\tableofcontents\clearpage
\section*{How to study with this guide}\phantomsection\label{study-method}
\markboth{How to study with this guide}{}
\addcontentsline{toc}{section}{How to study with this guide}
Studying with this guide should leave you with two things. The first is competence: a pathway is mastered when you can do what its outcome states and pass its checkpoint, not when every reading has been opened. The second is a reference: a compiled LaTeX compendium, in the manner of Wasserman's \emph{All of Statistics} (a reading in the \hyperref[route-common-toolkit]{common toolkit}), that states the definitions, conventions, results, models, methods, market mechanics, evidence, data and rules behind every part of this guide in one notation, with each statement traced to a located passage in its source. An experienced practitioner should be able to look a topic up in it, rely on each statement as far as its status allows, and follow its links to the same economics in other markets.

The method makes the reference a by-product of studying without letting it slow study down. Notes are written once, in three layers, and consolidated over several passes. Each pathway therefore has two milestones, kept apart: you \emph{master} it in one study loop, and you \emph{consolidate} its material into the compendium later, usually a section at a time. Entries are written in LaTeX from their first draft, so the compendium compiles at every stage, and fixed headings, one house notation, typed entries with stable labels and citations by catalogue key make consolidating it a matter of editing entries, not rewriting notes.

\subsection*{Keys, layers and registers}
Two keys tie notes to this guide and the catalogue. A reading's \emph{catalogue key} is printed at the right of its title in every reading list (for example \texttt{s6-pbo}); it is also the reading's link destination. For an optional branch or any other catalogue entry, follow the entry's \emph{Version record} link: the key is the part of the address after \texttt{\#}. A \emph{pathway key} is printed at the right of the navigation line that ends each overview route and specialist pathway. An overview route's key doubles as its section key. Section and subsection numbers can change between editions of this guide; keys do not. Name files and cite by key, never by number or page.
\par\Needspace{12\baselineskip}
\begin{center}\begin{tabular}{@{}P{2.4cm}P{4.3cm}P{3.3cm}P{6.6cm}@{}}
\toprule
\textbf{Layer} & \textbf{Unit} & \textbf{Written} & \textbf{Role} \\
\midrule
Reading note & One Markdown file per reading, named by catalogue key & During and straight after the reading & A faithful account of one source, translated into house notation. \\
Pathway note & One Markdown file per pathway, named by pathway key & When the checkpoint is done & How the readings fit together, the checkpoint answer, the entries the pathway created or changed, and its entry backlog. \\
Compendium entry & One LaTeX environment per concept, in the chapter of the section that is its home & Drafted per pathway; consolidated per section and part & A typed, labelled, self-contained statement with its sources: the unit of the compiled reference. \\
\bottomrule
\end{tabular}\end{center}
Four registers sit beside the layers: the \emph{notation register} (symbols, units, conventions and declared overrides); the \emph{glossary} (terms, acronyms and each market's name for them); the \emph{coverage log} (for each pathway, the dates it was mastered and consolidated, the checkpoint artefact and the entries produced); and the \emph{open-questions log}. The notation register and glossary open the compendium; the two logs share one Markdown file beside the notes. Each layer cites the one beneath it. Entries cite readings by catalogue key and locator, and pathway notes list entry labels, so any statement in the compiled reference can be traced to a passage in a source, and any source to every statement that relies on it.

\subsection*{The study loop}
Run one loop per pathway, and one for each section overview.
\begin{enumerate}
\item \textbf{Place yourself.} Read the pathway's outcome, prerequisites and checkpoint, then attempt the checkpoint before reading, from what you already know. What you can do, draft directly as compendium entries to verify against the readings; what you cannot do sets the questions to read for. Check prerequisites honestly: a gap there costs more time later than it saves now. For an overview whose checkpoint is marked as a section capstone, read the checkpoint now to see where the section is heading, and attempt it once you have mastered the pathways it names.
\item \textbf{Search before writing.} Look the pathway's topics up in the compendium and glossary, so that reading updates existing entries rather than duplicating them. Open the pathway note with your questions and the labels of the entries you expect to touch.
\item \textbf{Read in passes.} First pass: abstract, introduction, headings, figures and conclusion, to identify the claim and whether the reading answers your questions. Second pass: the core argument, model or empirical design and the main results, taking notes. Third pass only where the outcome needs it: work through the derivations or rebuild the estimation yourself. On familiar ground, read for the difference: what is new to you, what contradicts your practice, and what puts a number on something you knew only qualitatively.
\item \textbf{Close the source and recall.} After each reading, write its note from memory first, then reopen the source to correct and complete it. The corrections show what you had not yet understood.
\item \textbf{Do the checkpoint.} Treat it as the test of the pathway. Where it involves data or code, produce a working artefact and keep it with the data vintage it used; where it is analytical, write the argument out in full. Return to the readings only for what you could not do. Passing it masters the pathway: date it in the coverage log.
\item \textbf{Synthesise and extract.} Write the pathway note. Write full entries for what the checkpoint used and for what placement showed you did not know; for everything else the readings support, familiar material included, add a stub to the pathway's entry backlog (see below).
\item \textbf{Review by recall, spaced out.} Revisit the pathway note and retrieval cards after about a day, a week and a month, and again when a later pathway lists this one as a prerequisite. Recall first and check second; rereading alone gives a false sense of mastery. Tag each card with the label of the entry it tests, so that revising an entry flags its cards.
\end{enumerate}

\subsection*{Mastery and consolidation}
A pathway reaches two milestones at different times, and the coverage log dates each.
\begin{itemize}[leftmargin=1.4em,itemsep=2pt,topsep=3pt]
\item \textbf{Mastered:} you can do what the outcome states, and you have passed the checkpoint from your own notes with the readings closed. This is the learning milestone. It is reached in one study loop, and it is the only milestone later pathways depend on.
\item \textbf{Consolidated:} everything the pathway's readings and checkpoint rely on is in the compendium, familiar material included, in entries whose claims have been checked against their locators, and the pathway's entry backlog is empty. This is the reference milestone. It is usually reached when the whole section is consolidated, and it never holds up study.
\end{itemize}
The \emph{entry backlog} keeps the first pass manageable without giving up a comprehensive reference. While a source is open, a stub takes a minute: a proposed label, a one-line statement, and the catalogue key with the locator where the source makes the statement, one stub per line:
\begingroup\fontsize{7.6}{9.2}\selectfont
\begin{verbatim}
- res:<label>: <one-line statement> \citep[<locator>]{<catalogue-key>}
\end{verbatim}
\endgroup
\noindent Finding that locator again months later costs far more. During the study loop, write full entries only for what the checkpoint used and what placement showed you did not know, and stub everything else, including what you already know well. Consolidation turns stubs into entries until the backlog is empty.

\textbf{Required readings and what you already know.} A required reading is one that a route's outcome and checkpoint are built on and that its compendium entries will cite. It is not an instruction to study again what you can already do. If you pass a checkpoint at placement, the pathway is mastered: give each required reading a first pass for what is new to you, study only the passages that change your answer, and stub the passages you will cite. The readings stay required for consolidation, because the compendium cites them for familiar material too. A prerequisite pathway counts as met when you can pass its checkpoint, however you learned it.

\subsection*{What to take from a reading}
In specialist pathways, the stage label beside each reading predicts what it contributes and which entry types it feeds. Overview readings are unlabelled; take from them the section's vocabulary and map.
\par\Needspace{12\baselineskip}
\begin{center}\begin{tabular}{@{}P{3.4cm}P{10.0cm}P{3.4cm}@{}}
\toprule
\textbf{Stage label} & \textbf{What to extract} & \textbf{Entry types} \\
\midrule
Foundations, Theory & Definitions, assumptions, results and the idea of each proof. & Definition, Result \\
Valuation & Pricing relations, state variables, calibration targets, sensitivities and hedges. & Model, Result, Example \\
Methods, Validation & Estimators, algorithms, test statistics, diagnostics and the conditions under which they are valid. & Method, Pitfall \\
Mechanics & Contract terms, cash-flow and settlement timelines, quoting and day-count conventions, rights and priorities. & Mechanism, Convention \\
Evidence, Counter-evidence & Findings with magnitudes, samples and research designs; replications and failures. & Evidence \\
Data & Coverage, fields, timestamps, revisions and vintages, known biases and licence terms. & Data \\
Implementation & Costs, capacity, operational dependencies and failure modes. & Method, Pitfall \\
Regulation, Governance & Rules with their jurisdiction, scope, effective date and status. & Rule \\
\bottomrule
\end{tabular}\end{center}
Less common labels, such as case study, legal claim or contract terms, map to the nearest row. Whatever the stage, absorb what transfers to new problems: the claim and its scope; the mechanism, meaning the economic reason the result should hold and who is on the other side of the trade or bears the risk; the assumptions and, for empirical work, the source of variation and the main threat to it; whether every input was available at decision time; magnitudes with units and uncertainty; and the conditions under which the result disappears.

Skim on first contact: literature reviews, exhaustive robustness tables, proofs of technical lemmas the outcome does not need, and implementation detail for tools or vendors you do not use. Return to them when a checkpoint or later pathway depends on them. Do not memorise point estimates; record them with their sample, and remember the direction, rough size and conditions.

\subsection*{Reading notes}
Keep one Markdown file per reading, named by its catalogue key. Open it with a metadata block that scripts can read, then use the same headings in every note so that readings can be compared.
\par\Needspace{9\baselineskip}
\begingroup\fontsize{7.6}{9.2}\selectfont
\begin{verbatim}
---
key: s6-pbo
pathways: [common-toolkit]
version: 2017 journal article, Journal of Computational Finance
sections: 1-4, 6
read: 2026-10-14
status: draft
---
\end{verbatim}
\endgroup
\par\Needspace{16\baselineskip}
\begin{center}\begin{tabular}{@{}P{3.0cm}P{14.0cm}@{}}
\toprule
\textbf{Heading} & \textbf{What to record} \\
\midrule
Question and claim & One or two sentences in your own words: what is asserted, and for which market, instrument and period. \\
Mechanism & Why the result should hold; who bears the risk or supplies the liquidity. \\
Method & Model, estimator or research design; key assumptions; the main threat to identification. \\
Data and timing & Sample, frequency and construction; what was known at decision time. \\
Key results & Magnitudes with units, uncertainty and sample, each with its locator: page, section, table, figure or equation. \\
Limits & Where the result fails, counter-evidence and the catalogue's qualifications. \\
Implementation & Costs, capacity, data requirements and operational dependencies. \\
Notation map & Each symbol the source uses differently from house notation, with its house equivalent. \\
Connections & Catalogue keys of readings this one extends, contradicts or relies on. \\
Entries & Labels of compendium entries this reading creates, changes or contradicts. \\
Open questions & What you could not follow or verify, and what you would test. \\
Retrieval cards & Three to eight question--answer pairs, each testing one idea. \\
\bottomrule
\end{tabular}\end{center}
Write in your own words. Quote only definitions and statements you need exactly, with their locators, and begin your own reading of a passage with \emph{Interpretation:} so that it is never mistaken for the author's claim. Leave a heading empty rather than padding it; an empty \emph{Limits} heading after the second pass is itself an open question. Make retrieval cards atomic and prefer \emph{why} and \emph{what if} questions over names and dates.

\subsection*{Pathway notes}
Keep one Markdown note per pathway, named by its pathway key, of about a page plus the checkpoint material. Record the outcome restated in your own words; how the readings fit together, where they agree, where they conflict and which assumption decides between them; the checkpoint answer, or a link to its artefact and the data vintage it used; the labels of the entries created or changed; the entry backlog; what changed in your view or practice; and the questions carried forward. Enter the milestone dates in the coverage log.

\subsection*{Compendium entries}
An entry is the unit of the compiled reference. Write each one to these rules.
\begin{itemize}[leftmargin=1.4em,itemsep=2pt,topsep=3pt]
\item \textbf{One concept, one home.} Each concept has one entry, in the section where this guide first needs it; other sections link to it rather than restating it. A market-specific variant is a separate entry that links to the general one.
\item \textbf{Lead with the answer.} The first sentence answers the lookup: the definition, result or convention, or the finding with its magnitude.
\item \textbf{Self-contained.} An entry reads on its own: symbols are house notation or defined in it, and prerequisites are linked.
\item \textbf{Sourced at the claim.} Every number, formula, convention and rule carries its citation in the sentence that states it, not in a list at the end; begin your own derivations and readings of a source with \emph{Interpretation:}.
\item \textbf{Conditional.} State when it holds (assumptions, market, period, regime, jurisdiction) and date anything that can change.
\item \textbf{Stable label.} Never reuse or rename a label. When entries merge or split, keep each old label as an extra \texttt{\textbackslash label} in the entry that now holds its content, so that links to it still resolve.
\end{itemize}
\par\Needspace{18\baselineskip}
\begin{center}\begin{tabular}{@{}P{2.0cm}P{1.2cm}P{13.6cm}@{}}
\toprule
\textbf{Type} & \textbf{Label} & \textbf{Must contain} \\
\midrule
Definition & \texttt{def:} & Term, symbol, units and formula; variants, and the different names markets use for it. \\
Convention & \texttt{conv:} & Market, venue or jurisdiction; the quoting, day-count, settlement, fixing or roll rule; as-of date. \\
Result & \texttt{res:} & Statement; assumptions; the idea of the proof or where to find it; what fails when an assumption fails. \\
Model & \texttt{mod:} & State variables; dynamics or pricing equation; parameters and calibration; sensitivities and hedges; known failures. \\
Method & \texttt{meth:} & Inputs, steps and outputs; assumptions; diagnostics; computational cost; failure modes. \\
Mechanism & \texttt{mech:} & Contract terms; cash-flow and settlement timeline; rights and priorities; who bears each risk. \\
Evidence & \texttt{ev:} & Finding; magnitude with units and uncertainty; market, sample and period; design; replication status and counter-evidence. \\
Data & \texttt{data:} & Provider and coverage; frequency and timestamps; revisions and vintages; known biases; licence. \\
Rule & \texttt{rule:} & The rule and its citation; jurisdiction and scope; effective date; status and pending changes. \\
Pitfall & \texttt{pit:} & The error; how it arises; the check that detects it; the remedy. \\
Example & \texttt{ex:} & A worked numerical example: inputs, steps, answer and a sanity check. \\
\bottomrule
\end{tabular}\end{center}
Write each entry in the LaTeX environment of its type, named \texttt{qf} followed by the type in lower case (\texttt{qfdefinition}, \texttt{qfresult} and so on), and give it these fields in order, each a paragraph opened by \texttt{\textbackslash qffield} and the field's name: \emph{Statement}, followed by the formal content (formula, algorithm, timeline or table); \emph{Notation}, only where the entry overrides the house register; \emph{Conditions}; \emph{Practice}, meaning how the entry is used in pricing, risk, sizing or execution, with typical magnitudes; \emph{Pitfalls}; \emph{See also}; \emph{Further reading}, for sources that treat the topic more fully but support no particular claim; \emph{Index}; and \emph{Status}. Omit a field only when it cannot apply.

\emph{Status} records three properties that change independently.
\begin{itemize}[leftmargin=1.4em,itemsep=2pt,topsep=3pt]
\item \textbf{Verification:} \emph{unchecked}; \emph{partly checked}, saying what was checked; \emph{checked} with a date, once every claim has been compared with the passage at its locator; or \emph{contested}, where sources conflict.
\item \textbf{Stability:} \emph{draft}, or \emph{stable} once its label, scope and links are settled and it compiles without warnings.
\item \textbf{Currency:} \emph{timeless} for an identity or theorem; otherwise \emph{as of} a date with its review cadence, or \emph{superseded} by another label.
\end{itemize}
A corrected source resets verification; an amended rule, a new data vintage or a changed convention resets currency; a merge or split resets stability. None of them resets the others.
\par\Needspace{38\baselineskip}An entry in source form. Each claim cites its source where it is made, and the entry declares the one notation override it uses:
\begingroup\fontsize{7.6}{9.2}\selectfont
\begin{verbatim}
\begin{qfresult}[Put--call parity (European options, dividend yield)]\label{res:put-call-parity}
\qffield{Statement} A European call less a European put on the same underlying, with the
same strike $K$ and expiry $T$, is worth a forward position struck at $K$
\citep[chap.~``Options on stock indices and currencies'']{s7-hulloptions}:
\[ C_t - P_t = S_t e^{-q\tau} - K e^{-r\tau}, \qquad \tau = T - t. \]

\qffield{Notation} Option-pricing override: $P_t$ is the put price and $r$ the continuously
compounded risk-free rate to $T$, not the register's bond price and log return.

\qffield{Conditions} No arbitrage; European exercise; a continuous dividend yield $q$;
borrowing and lending at $r$. American options satisfy only bounds
\citep[chap.~``Properties of stock options'']{s7-hulloptions}.

\qffield{Practice} Interpretation (own derivation): rearranged, parity gives the
option-implied forward $F_t = K + (C_t - P_t)e^{r\tau}$, and with it the dividend yield or
borrow cost that a call--put pair implies. In one study, deviations from parity, measured as
the implied-volatility gap between matched calls and puts, predicted the underlying stocks'
returns: stocks with relatively expensive calls outperformed stocks with relatively
expensive puts by 50 basis points a week. The authors report that the result was not driven
by hard-to-borrow stocks and that the predictability decreased over their sample
\citep[abstract]{eq-cremers-weinbaum-2010}.

\qffield{Pitfalls} Discrete dividends; early exercise; stale or non-synchronous quotes.

\qffield{See also} \hyperref[res:covered-interest-parity]{Covered interest parity}
(currency analogue); \hyperref[res:cash-and-carry]{cash-and-carry} (commodity analogue,
with convenience yield).

\qffield{Index} put--call parity; conversion; reversal; synthetic forward; implied forward

\qffield{Status} Verification: partly checked 2026-10-14 (the evidence against its abstract;
the textbook's chapter titles against the publisher's contents for this edition, not the
text). Stability: draft. Currency: identity timeless; evidence as published in 2010.
\end{qfresult}
\end{verbatim}
\endgroup
The status says no more than was checked: the formulas have not yet been compared with the textbook's text, so the entry is not yet \emph{checked}, however standard they are.

\subsection*{House notation and units}
Fix notation before the first note and keep it in the notation register. Change it only through the register, never silently, and translate each source into house notation in its reading note's notation map. Where a market quotes in its own convention, such as a rate's compounding or a volatility quoted in normal rather than lognormal terms, record the convention in a Convention entry and convert explicitly in formulas. A starting register:
\par\Needspace{12\baselineskip}
\begin{center}\begin{tabular}{@{}P{2.8cm}P{14.2cm}@{}}
\toprule
\textbf{Quantity} & \textbf{Convention} \\
\midrule
Time & $t$ now, $T$ maturity or horizon, $\tau = T - t$ in years, with the day count used to compute $\tau$. \\
Prices & $S$ spot or underlying, $F$ forward or futures, $P$ bond price, $V$ value of a claim, $K$ strike; currency stated. \\
Returns & $R$ simple, $r = \ln(1+R)$ log; excess returns written explicitly as $R - R_f$; frequency stated, and whether annualised. \\
Rates and yields & Compounding (continuous, annual, semi-annual or simple) and day count named with every formula; spreads in basis points. \\
Volatility & $\sigma$ annualised, with the annualisation factor and the return type stated; variance written as $\sigma^2$. \\
Probability & $\mathbb{P}$ physical and $\mathbb{Q}$ risk-neutral, marked on every expectation, as in $\mathbb{E}^{\mathbb{Q}}_t[\cdot]$. \\
Signs & P\&L positive is a gain to the holder; sides named explicitly: long or short, payer or receiver, protection buyer or seller. \\
Time stamps & ISO 8601 dates; times with their time zone and clock (exchange time or UTC). \\
\bottomrule
\end{tabular}\end{center}
\textbf{Local overrides.} Some symbols mean different things in different fields: $r$ is a log return in econometrics and the risk-free rate in option pricing, and $P$ is a bond price in rates and a put price in options. Where a field's own convention is near universal, follow it rather than translate every source. Declare the override at the start of the chapter, in its \texttt{section.tex}, for every entry in that chapter, or in an entry's \emph{Notation} field, for that entry alone, and list it in the register with its scope. Never override silently, never use both meanings in one entry, and write the house meaning out in full where an overridden chapter needs it, as $\ln(1+R)$ for a log return. The example above declares the option-pricing override.

\subsection*{Cross-references}
The compendium is used by looking things up, so it must link in every direction.
\begin{itemize}[leftmargin=1.4em,itemsep=2pt,topsep=3pt]
\item \textbf{Between entries,} by label: \texttt{\textbackslash hyperref[res:put-call-parity]\{text\}}, and to a numbered equation with \texttt{\textbackslash eqref\{eq:}\emph{name}\texttt{\}}. Never type an entry's number or page.
\item \textbf{To sources,} one key and one locator per citation: \texttt{\textbackslash citep[locator]\{key\}}. The locator is a page, section, equation, table or figure; for a rule, the article or paragraph; for data, the field and vintage; for a paper checked only against its abstract, \emph{abstract}. Name book chapters by title, not number. Give a source outside the catalogue a key in the same style and a line in the compendium's sources file until it is catalogued.
\item \textbf{With a reason.} Say why each \emph{See also} link is there: prerequisite, generalisation or special case, contrast or contradiction, or cross-asset analogue.
\item \textbf{Across markets.} The same economics recurs under different names, and linking it is what a cross-market reference adds to its sources. The cost of carry and its frictions appear as repo specialness in government bonds, borrow fees in equities, convenience yield in commodities, the cross-currency basis in currencies and funding rates on perpetual futures; dealer inventory risk appears in bond, currency, equity and crypto market making.
\item \textbf{Through the index and glossary.} List index terms in every entry, including synonyms and each market's name for the concept. Use the glossary for terms that change meaning between desks: \emph{basis}, \emph{carry}, \emph{roll} and \emph{convexity} mean different things in rates, commodities, currencies and options.
\item \textbf{Back to this guide.} Open each compendium chapter with the pathway keys it draws on; each pathway note already lists the entries it produced.
\end{itemize}

\subsection*{Passes: from notes to a compiled reference}
Notes reach the compiled reference in passes. Each pass moves pathways towards their milestones and raises one part of the status of the entries it touches.
\begin{enumerate}
\item \textbf{Capture,} for each pathway during the study loop: reading notes, the pathway note with its entry backlog, the checkpoint artefact, and entries drafted or updated. New entries are unchecked drafts. Compile the compendium at the end of each loop, so that a broken link or LaTeX error surfaces while it is small. The pathway is mastered when its checkpoint is passed.
\item \textbf{Consolidate,} for each section once its pathways are mastered. Work every backlog into entries and merge duplicates into their home entries. Where sources conflict, keep both findings with their conditions instead of averaging them, and mark the entry contested. Normalise notation. Check every number, formula, convention and rule against the passage at its locator, and date the check. Write the chapter's opening paragraph from the section goals, and build quick-reference tables (formulas, conventions by market, evidence with magnitudes, checklists) only from checked entries, citing their labels so that the tables cannot drift. A pathway whose backlog is empty and whose entries are checked is consolidated.
\item \textbf{Integrate,} for each part and then the whole guide. Add cross-section and cross-asset links, complete the glossary and each entry's index terms, and resolve every undefined reference the compiler reports. Then work each pathway's checkpoint again from the compendium alone, data apart: anything for which you still need a source is a missing entry. Entries that are cross-referenced and compile without warnings become stable.
\item \textbf{Maintain,} whenever you move the notes to a newer edition of this guide, and on the catalogue's review cadence; see below.
\end{enumerate}
An entry is finished when it has a type, a label, a statement and a status; uses house notation or declares its overrides; cites a locator at every claim; states its conditions; dates whatever can change; and has no unresolved links, stubs or to-do marks. A chapter is complete when every pathway in its section is consolidated and its entries are stable.

\subsection*{Maintaining the compendium}
Maintenance asks three questions of each entry separately, because their answers change for different reasons: was it \emph{verified} against its sources, is it \emph{stable} as written, and is it still \emph{current}? A new edition of this guide can change the sources and the routes; the passage of time alone can make an entry out of date.

\textbf{When the guide changes.} Before moving the submodule from one edition, \texttt{OLD}, to another, \texttt{NEW} (both commits), list what changed. Comparing \texttt{catalogue\_recency.json} is not enough: it exports version records and links, so a corrected annotation, a changed qualification or a new extended note leaves it unchanged. Compare the catalogue source itself, in which every entry, extended note and version record fills exactly one line (the generator enforces this), and compare the route definitions by key:
\par\Needspace{20\baselineskip}
\begingroup\fontsize{7.6}{9.2}\selectfont
\begin{verbatim}
cd guide
git diff -U0 OLD NEW -- institutional_quantitative_finance_reading_list.tex |
  grep -oE '^[-+]\\(CatalogueEntry|EntryRecency|ExtendedNote)\{[^}]+\}' |
  sed -E 's/.*\{(.*)\}/\1/' | sort -u                      # catalogue keys to revisit
python3 - OLD NEW <<'EOF'                                   # pathway keys to reopen
import json, subprocess, sys
def routes(rev):
    text = subprocess.run(['git', 'show', rev + ':learning_routes.json'],
                          capture_output=True, text=True, check=True).stdout
    data = json.loads(text)
    return {r['id']: r for r in data['routes'] + data['specialist_routes']}
old, new = routes(sys.argv[1]), routes(sys.argv[2])
for key in sorted(old.keys() | new.keys()):
    if old.get(key) != new.get(key):
        print(key, 'added' if key not in old else 'removed' if key not in new else 'changed')
EOF
\end{verbatim}
\endgroup
For each listed catalogue key, search the notes and the compendium for it, with \texttt{grep -rnwF} \emph{key} \texttt{notes compendium}, and read the changed record: a new edition or a correction resets the verification of every entry that cites the key, and a retraction or a superseding source may remove a claim. For each listed pathway key, compare its outcome, section goals, readings and checkpoint with your pathway note, and reopen the pathway in the coverage log if they changed after you mastered it. If the new edition prints a different \texttt{house.tex}, replace your copy with it and recompile.

\textbf{As time passes.} Review the currency of dated entries on the catalogue's cadence: quarterly for rules, protocols, software and preliminary papers; with each data vintage; and annually for published research and books. A catalogue version record says when the catalogue last verified a source and against what (metadata, abstract or full text). It supports your own check but does not replace it: an entry is verified only against the passages you compared it with, and current only as of the date you last reviewed it.

\subsection*{Files and compiling the reference}
Keep the notes in a repository of their own, as plain text under version control, so that they stay searchable, comparable across versions and portable between tools. Catalogue keys and pathway keys are the interface between that repository and this guide's. Add this guide's repository to the notes as a git submodule: it pins the edition the notes follow, keeps the catalogue and its version records beside the notes for links and comparisons, and changes only when you move it. Write reading and pathway notes in Markdown, which is quick to write and never compiled, and compendium entries directly in LaTeX, so that the reference compiles as written. In both, write mathematics and citations as an entry does, so that a passage moves from a note into an entry unchanged.
\par\Needspace{14\baselineskip}
\begingroup\fontsize{7.6}{9.2}\selectfont
\begin{verbatim}
guide/                                  this guide's repository, pinned as a git submodule
notes/readings/<catalogue-key>.md       one note per reading
notes/pathways/<pathway-key>.md         one note per pathway, with its entry backlog
notes/artefacts/<pathway-key>/          checkpoint code, derivations and data vintages
notes/log.md                            coverage log (milestone dates) and open questions
compendium/compendium.tex               master file: one chapter per section, in this guide's order
compendium/preamble.tex                 your own packages and macros; may be empty
compendium/house.tex                    entry environments, citations and sources, printed below
compendium/front/notation.tex           notation register and overrides; glossary.tex beside it
compendium/front/sources.tex            sources outside the catalogue, one line per key
compendium/<section-key>/section.tex    a chapter: its heading and pathway keys, then its topic files
compendium/<section-key>/<topic>.tex    entries, grouped under section headings
compendium/<section-key>/figures/       the chapter's figures
\end{verbatim}
\endgroup
Write compendium files so that they compile without editing:
\begin{itemize}[leftmargin=1.4em,itemsep=2pt,topsep=3pt]
\item Open each \texttt{section.tex} with the section's name as a chapter heading labelled by its section key, as in \texttt{\textbackslash chapter\{Systematic equities\}\textbackslash label\{systematic-equities\}}, then the pathway keys it draws on, then an \texttt{\textbackslash input} line for each topic file, named from \texttt{compendium/}. Group entries under section headings; entries themselves are not headings.
\item Give each entry's name as the optional argument of its environment and put its label straight after it, as in the example. Titles may contain ordinary punctuation and inline mathematics.
\item Number an equation only when something refers to it, and give it an \texttt{eq:} label. Use LaTeX commands rather than Unicode mathematical symbols, which pdflatex cannot always set.
\item Cite a source as \texttt{\textbackslash citep[}\emph{locator}\texttt{]\{}\emph{key}\texttt{\}}; like a catalogue key, a key contains only lower-case letters, digits and hyphens. Give each source outside the catalogue a line \texttt{\textbackslash qfsource\{}\emph{key}\texttt{\}\{}\emph{full reference}\texttt{\}} in \texttt{front/sources.tex}, and cite its key like any other.
\item Keep each figure in its chapter's \texttt{figures/} folder and include it by its path from \texttt{compendium/}, such as \texttt{systematic-equities\slash figures\slash smile}.
\end{itemize}
The two files below were compiled on 14 October 2026 with pdflatex (TeX Live 2023) into a sample compendium with all eleven entry types, titles containing ampersands, colons, dashes and mathematics, links between entries and to equations, citations of catalogue keys and of a source outside the catalogue, and a figure in its chapter's folder, with no errors, warnings, undefined references or overfull lines. \texttt{house.tex} declares the eleven environments with one numbering per chapter and titles that wrap like a paragraph; defines \texttt{\textbackslash citep} to link a key to its line in the sources if it has one, and otherwise to its entry in the pinned catalogue PDF, as this guide's reading links do; and defines \texttt{\textbackslash qfsections}, which includes a section's chapter once its \texttt{section.tex} exists. Keep your own packages and macros in \texttt{preamble.tex} and leave \texttt{house.tex} unedited, so that a new edition can replace it; do not load natbib or biblatex, because \texttt{house.tex} defines \texttt{\textbackslash citep} itself.
\par\Needspace{34\baselineskip}
\begingroup\fontsize{7.6}{9.2}\selectfont
\begin{verbatim}
% compendium/house.tex: entry environments, citations and sources, as printed in the
% learning guide. compendium.tex loads it after your preamble; replace it, do not edit it.
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,booktabs,graphicx,hyperref}
\hypersetup{colorlinks}
\setlength{\emergencystretch}{3em}   % lets a line holding a long key break
\newcounter{qfentry}[chapter]
\renewcommand{\theqfentry}{\thechapter.\arabic{qfentry}}
% \qftype{type}{Name} declares the environment qf<type>; its title wraps like a paragraph.
\newcommand{\qftype}[2]{\newenvironment{qf#1}[1][]{\par\addvspace{\medskipamount}%
  \refstepcounter{qfentry}{\raggedright\noindent\bfseries #2 \theqfentry
  \if\relax\detokenize{##1}\relax\else\quad ##1\fi\par}\nopagebreak}%
  {\par\addvspace{\medskipamount}}}
\qftype{definition}{Definition}\qftype{convention}{Convention}\qftype{result}{Result}
\qftype{model}{Model}\qftype{method}{Method}\qftype{mechanism}{Mechanism}
\qftype{evidence}{Evidence}\qftype{data}{Data}\qftype{rule}{Rule}
\qftype{pitfall}{Pitfall}\qftype{example}{Example}
\newcommand{\qffield}[1]{\par\textbf{#1.}\enspace}   % starts one of an entry's fields
% \citep[locator]{key} links the key to its line in the sources if it has one,
% and otherwise to its entry in the pinned catalogue PDF.
\newcommand{\qfcatalogue}{../guide/institutional_quantitative_finance_reading_list.pdf}
\NewDocumentCommand{\citep}{o o m}{[\IfValueT{#2}{#1 }%
  \ifcsname r@src:#3\endcsname\hyperref[src:#3]{\texttt{#3}}%
  \else\href{\qfcatalogue\##3}{\texttt{#3}}\fi
  \IfValueTF{#2}{, #2}{\IfValueT{#1}{, #1}}]}
% \qfsource{key}{reference} records one source outside the catalogue, in front/sources.tex.
\newcommand{\qfsource}[2]{\par\noindent\phantomsection\label{src:#1}\texttt{#1}\quad #2\par}
% \qfsections{key, ...} inputs <key>/section.tex for each listed key that has one, in order.
\ExplSyntaxOn
\NewDocumentCommand{\qfsections}{m}
  {\clist_map_inline:nn {#1} {\InputIfFileExists{##1/section}{}{}}}
\ExplSyntaxOff
\end{verbatim}
\endgroup
\par\Needspace{24\baselineskip}
The master file lists every section key in this guide's order, so a chapter takes its place as soon as its \texttt{section.tex} exists. Compile it from \texttt{compendium/} with \texttt{latexmk -pdf compendium.tex}:
\begingroup\fontsize{7.6}{9.2}\selectfont
\begin{verbatim}
% compendium/compendium.tex: compile inside compendium/ with  latexmk -pdf compendium.tex
\documentclass[a4paper,oneside,openany]{book}
\input{preamble}
\input{house}
\pagestyle{plain}                    % section names are too long for running heads
\begin{document}
\frontmatter
\tableofcontents
\input{front/notation}
\InputIfFileExists{front/glossary}{}{}
\mainmatter
SECTION_KEY_LIST
\backmatter
\chapter{Sources outside the catalogue}
\input{front/sources}
\end{document}
\end{verbatim}
\endgroup
\textbf{Notes written before this method.} File existing notes by the section key of their home, as a \texttt{section.tex} and topic files, and keep them compiling, with any environments they use declared in \texttt{preamble.tex} and their citations changed to catalogue keys or lines in the sources file. Treat their blocks as entry backlog for the pathways that cover them: when you consolidate a pathway, rewrite each block as an entry of the type its content calls for, whatever its old environment was called, with a label, a citation at each claim and a status, and delete the old block. For a book you read before starting, record your progress against its catalogue key in the coverage log, and write its reading note when a pathway first lists it.

\textbf{Working now, and proposed.} Everything printed above works as it stands. Three pieces of tooling are proposals, not yet built: a BibTeX export of the catalogue, so that the compendium can print a bibliography rather than link each key to the catalogue; a printed index built from the \emph{Index} fields (until then each prints as a keyword line in its entry); and a checker that reports dangling labels, stubs left in entries and claims without a citation.

\subsection*{Using LLMs}
Use a language model as a tutor and sparring partner after you have read, not as a substitute for reading. Fluent answers are not evidence: models misstate results, invent citations, formulas and numbers, and may not know recent papers, editions or rule changes.

\textbf{Productive uses.}
\begin{itemize}[leftmargin=1.4em,itemsep=2pt,topsep=3pt]
\item \textbf{Explain differently:} paste a passage and ask for an explanation at a stated level, a worked numerical example or the intuition behind one step.
\item \textbf{Fill prerequisite gaps:} ask for a short derivation or toy example of an assumed concept, then confirm it in a foundation reading.
\item \textbf{Test yourself:} give it your note and ask it to quiz you one question at a time, without revealing answers, concentrating on your weakest heading.
\item \textbf{Critique your work:} ask it to attack your checkpoint answer or research record for look-ahead bias, multiple testing, omitted costs and identification threats, naming the assumption each objection targets.
\item \textbf{Check derivations and code:} ask for a line-by-line check of a derivation, or a review of replication code for timing and data errors; run the code and tests yourself.
\item \textbf{Consolidate:} give it a set of entries and the notation register, and ask for duplicates, contradictions, departures from house notation, unstated conditions and missing links. Decide each change yourself.
\item \textbf{Convert and debug:} ask it to recast part of a note as a LaTeX entry of the right type, or to diagnose a LaTeX error, then compare the result with the original line by line.
\item \textbf{Draft retrieval cards and index terms:} generate candidates from your own note or entry, then edit them.
\end{itemize}
\textbf{Rules.}
\begin{itemize}[leftmargin=1.4em,itemsep=2pt,topsep=3pt]
\item \textbf{Attempt first.} Write your own answer, derivation or note before asking, so the model corrects your understanding rather than replacing it.
\item \textbf{Ground it in the text.} Paste the relevant section, ask it to answer only from that text and to cite the section, page or equation; treat anything it cannot locate as unverified.
\item \textbf{Verify before recording.} Never copy a reference, number, formula or regulatory fact from a model into your notes without checking it in the primary source or the catalogue. Nothing a model writes enters an entry's statement, magnitudes or sources without a locator you have checked yourself.
\item \textbf{Protect confidential material.} Do not paste proprietary data, positions, code or licensed full texts into tools your institution has not approved.
\end{itemize}
\textbf{Example prompts.}
\begin{quote}\small
I am studying [reading] for this outcome: [pathway outcome]. Below are section [n] and my note on it. Using only the text: (1) identify errors or gaps in my note; (2) ask me three questions, one at a time, that test the mechanism and its assumptions; (3) mark anything you cannot support from the text as unverified.
\end{quote}
\begin{quote}\small
Below are my notation register and the entries [labels]. Without adding facts: (1) list entries that duplicate or contradict each other; (2) list symbols or units that depart from the register; (3) list conditions a reader would need that an entry omits; (4) suggest \emph{See also} links, each with a one-line reason. Quote the text that supports each point.
\end{quote}
\clearpage
\section*{Using the routes}
\markboth{Using the routes}{}
The guide progresses through PART_COUNT parts. Each numbered section starts with an overview route; its specialist pathways follow immediately as numbered subsections. Start with the common toolkit and research process, then choose a subject branch using the \hyperref[learning-map]{learning pathway DAG}. The contents and PDF bookmarks expose the same part, section and subsection hierarchy. All digital-asset applications are together in Part VI, including dealer execution and options; links bring in their earlier foundations.

\textbf{Overviews: orientation and completion.} An overview route opens each section. Its \emph{section goals} list what the section's pathways teach, each with the pathways that teach it. Its \emph{overview outcome} is narrower: what its own readings deliver, stated so that its checkpoint can test it. Read an overview's readings for orientation before its pathways: their questions, vocabulary and main results, and where each pathway fits, which are the first two passes of the study loop. Every pathway in the section assumes that orientation and no more, and so does a route in another section that lists the overview among its prerequisites; a route that needs a pathway's methods lists that pathway. Completing an overview means passing its checkpoint. Most overview checkpoints can be done straight after the readings. Where one uses methods that the section's own pathways teach, it is marked as a \emph{section capstone}, with the pathways to complete first, and it closes the section rather than opening it.

\textbf{Pathways, readings and checkpoints.} Read each selected sequence in order and complete its checkpoint. \emph{Required} readings are those a route's outcome and checkpoint are built on and that its compendium entries cite; if you can already pass the checkpoint, read them for what is new and for their locators rather than studying them again (see \hyperref[study-method]{How to study with this guide}). Prerequisites identify assumed knowledge rather than a compulsory schedule, and a prerequisite pathway is met when you can pass its checkpoint. Stage labels identify mechanics, valuation, empirical evidence, data and implementation; the number of readings follows the subject rather than a fixed cap. Optional branches extend a topic without adding to the required set. Book selections identify topics or chapters only where the catalogue supports them; no chapter numbers or workload estimates are inferred. A paired-paper entry is marked explicitly when the route uses only one of its works. A checkpoint is a learning exercise, not evidence of investment performance or readiness for live trading.

\textbf{Diagrams.} The \hyperref[learning-map]{learning pathway DAG} that follows shows every section, part by part. Begin with the shared foundations in Part I; the dashed connector from the common toolkit leads to every subject part. Solid arrows show the recommended study order within each row; they do not require every section to be completed. Each node links to its numbered section and each part label to its part opener. Consult the linked prerequisites before moving between branches: for example, FX options build on options knowledge, private-credit work uses public-credit foundations, and crypto derivatives use both options and venue mechanics. Every section with two or more specialist pathways also has its own DAG, showing its in-section dependencies, the earlier foundations each pathway brings with it and any capstone checkpoint: SECTION_DAG_INDEX

Reading titles link to the \href{institutional_quantitative_finance_reading_list.pdf}{canonical reference catalogue}. Edition, publication status, primary links and full qualifications live there. This guide's title text is generated from the catalogue, while route choices and rationales are maintained separately. Keep the two PDFs and the extended-notes HTML together. PDF links work in viewers that support named destinations in companion files; a catalogue page is also supplied for every reading and branch.

Research or preliminary status does not make a work an advanced prerequisite or an endorsement. Treat empirical findings as conditional on their sample, design and implementation assumptions. Use the catalogue's foundations and counter-evidence when a result is unfamiliar or disputed.
''']
    pathway_date=date.fromisoformat(route_data['pathway_updated_on'])
    pathway_display=f'{pathway_date.day} {pathway_date.strftime("%B %Y")}'
    dag_sections=[r['id'] for part in parts for r in (overviews[i] for i in part['routes']) if len(r['specialist_order'])>=2]
    dag_index='; '.join('\\hyperref['+section_dag_label(i)+']{'+tex_escape(overviews[i]['name'])+'}' for i in dag_sections)+'.'
    section_keys=', '.join(k for part in parts for k in part['routes'])
    section_key_list=textwrap.fill(section_keys,width=88,initial_indent='\\qfsections{',subsequent_indent='  ',break_on_hyphens=False,break_long_words=False)+'}'
    guide[-1]=guide[-1].replace('SECTION_KEY_LIST',section_key_list)
    guide[-1]=guide[-1].replace('SECTION_DAG_INDEX',dag_index).replace('ROUTE_SUMMARY',tex_escape(route_summary)).replace('EDITION_DATE',display_date).replace('PATHWAY_DATE',pathway_display).replace('PART_COUNT_CAP',PART_WORDS[len(parts)].capitalize()).replace('PART_COUNT',PART_WORDS[len(parts)])
    if html_links:
        old_intro=guide[-1].index('Reading titles link to')
        end_intro=guide[-1].index('\n\nResearch or preliminary',old_intro)
        guide[-1]=guide[-1][:old_intro]+r'''Reading titles and optional branches link to the \href{catalogue_extended_notes.html}{current catalogue notes and version records}. Keep that HTML companion with this guide. The canonical catalogue source owns citations and qualifications; this guide adds the reading order and exercises. The editor preview reflects the current source. Saved PDFs are earlier snapshots until explicitly exported again, so their page numbers are not used here. A browser or viewer that permits local companion links is required.'''+guide[-1][end_intro:]
    # Read resolved page numbers from aux; explicit named destinations are in out/pdf.
    pages={} if html_links else page_destinations()
    guide.append(overview_chart(parts,all_routes))
    ordered=[]
    for part in parts:
        ordered.append(('part',part))
        for identifier in part['routes']:
            r=overviews[identifier]
            ordered.append(('overview',r))
            ordered.extend(('specialist',all_routes[sid]) for sid in r['specialist_order'])
    for kind,r in ordered:
        if kind=='part':
            guide.append('\\clearpage\n\\part{'+tex_escape(r['title'])+'}\\label{part-'+r['id']+'}\n'+tex_escape(r['introduction'])+'\n\n')
            guide.append('\\textbf{Sections in learning order}\\begin{enumerate}\n')
            for identifier in r['routes']:
                route=overviews[identifier]
                guide.append('\\item[\\ref*{route-'+identifier+'}.] '+route_link(identifier,all_routes)+' --- '+tex_escape(route['learning_note'])+'\n')
            guide.append('\\end{enumerate}\n\\hyperref[learning-map]{Return to the learning pathway DAG.}\n')
            continue
        is_overview=kind=='overview'
        label=('route-' if is_overview else 'specialist-')+r['id']
        heading='section' if is_overview else 'subsection'
        guide.append(('\\clearpage' if is_overview else '\\Needspace{12\\baselineskip}')+'\n\\'+heading+'{'+tex_escape(r['name'])+'}\\label{'+label+'}\n')
        if is_overview:
            guide.append('\\label{'+r['legacy_label']+'}\n')
            guide.append('\\textbf{Learning sequence.} '+tex_escape(r['learning_note'])+'\n\n')
            guide.append('\\textbf{Section goals.} Across its pathways, this section teaches you to:\n\\begin{itemize}[leftmargin=1.4em,itemsep=0pt,topsep=1pt]\n')
            for g in r['section_goals']:
                guide.append('\\item '+tex_escape(g['goal'])+' ('+', '.join(number_link(p,all_routes) for p in g['pathways'])+')\n')
            guide.append('\\end{itemize}\n')
        else:
            guide.append('\\textbf{Specialist pathway.} In '+route_link(placement[r['id']],all_routes)+'.\n\n')
        guide.append('\\textbf{'+('Overview outcome' if is_overview else 'Outcome')+'.} '+tex_escape(r['outcome'])+'\n\n\\textbf{Prerequisites.} '+tex_escape(r['prerequisites'])+'\n\n')
        prerequisites=r.get('prerequisite_routes',[])
        if prerequisites:
            guide.append('\\textbf{Review first.} '+'; '.join(route_link(identifier,all_routes) for identifier in prerequisites)+'.\n\n')
        guide.append('\\textbf{Required readings, in order}\n\\begin{enumerate}\\raggedright\n')
        for rd in r['required_readings']:
            rec=by_anchor[rd['anchor']];a=rec[0];title=unlinked(rec[1])
            page=pages.get(a)
            destination=('catalogue_extended_notes.html' if html_links else CATALOGUE+'.pdf')+'\\#'+a
            guide.append('\\Needspace{5\\baselineskip}\\item \\href{'+destination+'}{'+title+'}')
            if page:guide.append('\\CataloguePage{'+str(page)+'}')
            guide.append('\\NoteKey{'+a+'}')
            if rd.get('selection'):guide.append('\\par\\emph{Selection:} '+tex_escape(rd['selection']))
            stage='\\textbf{'+tex_escape(rd['stage'])+'.} ' if rd.get('stage') else ''
            guide.append('\\par '+stage+tex_escape(rd['reason'])+'\n')
        capstone=r.get('checkpoint_after',[])
        checkpoint='Checkpoint'+(', a section capstone: complete it after '+and_list([number_link(p,all_routes) for p in capstone]) if capstone else '')
        guide.append('\\end{enumerate}\n\\Needspace{5\\baselineskip}\\textbf{'+checkpoint+'.} '+tex_escape(r['checkpoint'])+'\n\n')
        branches=[]
        for b in r['optional_branches']:
            a=b['target'];dest=a if html_links else labels.get(a,a)
            if a in by_anchor:dest=by_anchor[a][0]
            page=pages.get(dest)
            branch='\\href{'+('catalogue_extended_notes.html' if html_links else CATALOGUE+'.pdf')+'\\#'+dest+'}{'+tex_escape(b['reason'])+'}'
            if page:branch+='\\BranchPage{'+str(page)+'}'
            branches.append(branch)
        if branches:guide.append('\\textbf{Optional branches.} '+' '.join(branches)+'\n')
        children=[all_routes[sid] for sid in r.get('specialist_order',[])]
        if children:
            guide.append('\\par\\textbf{Continue in this section.} '+'; '.join(route_link(s['id'],all_routes) for s in children)+'.\n')
        elsewhere=[s for s in specialists if s['parent_route']==r['name'] and placement[s['id']]!=r['id']]
        if elsewhere:
            guide.append('\\par\\textbf{Digital-asset applications (Part VI).} '+'; '.join(route_link(s['id'],all_routes) for s in elsewhere)+'.\n')
        guide.append('\\par{\\small \\hyperref[learning-map]{Learning pathway DAG}')
        if not is_overview:
            guide.append(' \\textbar{} '+route_link(placement[r['id']],all_routes,'Section overview'))
        section_id=r['id'] if is_overview else placement[r['id']]
        if section_id in dag_sections:
            guide.append(' \\textbar{} \\hyperref['+section_dag_label(section_id)+']{Section DAG}')
        guide.append('\\NoteKey{'+r['id']+'}}\n')
        if is_overview and r['id'] in dag_sections:
            guide.append(section_chart(r['id'],overviews,all_routes))
    guide.append('\\end{document}\n')
    (ROOT/(GUIDE+'.tex')).write_text(''.join(guide))

    note_titles={r[0]:r[1] for r in records}
    subject_titles={}
    # Subject notes are local to the immediately preceding canonical heading.
    current=''
    for line in source.splitlines():
        m=re.match(r'\\section\{(.+?)\}',line)
        if m:current=m[1]
        m=re.match(r'\\ExtendedNote\{(subject-[^}]+)\}',line)
        if m:subject_titles[m[1]]=current
    document=['''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quantitative finance — extended catalogue notes</title>
<style>body{font:17px/1.65 system-ui,sans-serif;color:#20333f;background:#faf9f6;max-width:850px;margin:50px auto;padding:0 24px}h1,h2{line-height:1.2}h1{font-size:38px}h2{font-size:23px}a{color:#1b5875;overflow-wrap:anywhere}article{border-top:1px solid #c9d1d5;padding:28px 0;scroll-margin-top:20px}article:target{border-left:4px solid #1b5875;padding-left:20px;background:#edf3f5}.meta{font-size:14px;color:#546570}nav{padding:16px 0}code{font-size:14px}input{font:inherit;padding:10px;width:95%;margin:16px 0}small{color:#546570}</style>
<h1>Catalogue notes and version records</h1><p>Annotations, material qualifications and structured recency records for every catalogue entry. Generated from the canonical LaTeX source; EDITION_DATE. Verification scope distinguishes newly inspected sources from inherited evidence and unverified fields. A verification date alone is not a full-text, legal-currentness or empirical validation claim.</p>
<nav>Companion PDFs: <a href="institutional_quantitative_finance_reading_list.pdf">Reference catalogue</a> · <a href="institutional_quantitative_finance_learning_guide.pdf">Learning guide</a>. Keep these PDFs and this HTML companion together.</nav>
<label for="search">Filter entries by title, topic, date or evidence</label><input id="search" type="search" placeholder="Search catalogue entries and version records"><p id="count"></p>''']
    document[0]=document[0].replace('EDITION_DATE',display_date)
    notes_by_id=dict(notes)
    # Current HTML destinations must not depend on an older saved PDF or aux.
    # Section labels land at their first following entry; citation aliases land
    # at their owning entry. Numbered sources are exported below.
    aliases={r[0]:[] for r in records}
    pending=[]
    for line in source[source.index('\\begin{document}'):].splitlines():
        pending.extend(re.findall(r'\\label\{([^}]+)\}',line))
        m=re.match(r'\\CatalogueEntry\{([^}]+)\}',line)
        if m:
            a=m[1]
            aliases[a].extend(pending);pending=[]
            aliases[a].extend(re.findall(r'\\hypertarget\{([^}]+)\}',by_anchor[a][1]))
    if html_links:
        document[0]=document[0].replace('Companion PDFs:', 'Earlier saved PDF snapshots:').replace('Keep these PDFs and this HTML companion together.', 'Use this HTML and the current source preview for the latest additions.')
        document[0]=document[0].replace('>Reference catalogue</a>','>Saved catalogue PDF snapshot</a>').replace('>Learning guide</a>','>Saved guide PDF snapshot</a>')
        document[0]=document[0].replace('<label for="search">','<p class="meta">Current source and editor preview include later gap-closure edits. The saved PDFs above have not been re-exported.</p>\n<label for="search">')
    display_notes=[(r[0],notes_by_id.get(r[0],r[5])) for r in records]
    display_notes += [(a,body) for a,body in notes if a not in by_anchor]
    for a,body in display_notes:
        title=note_titles.get(a,subject_titles.get(a,'Subject context'))
        document.extend('<span id="'+html.escape(alias,quote=True)+'"></span>' for alias in aliases.get(a,[]) if alias!=a)
        document.append('<article id="'+html.escape(a,quote=True)+'"><h2>'+to_html(title,labels)+'</h2>')
        if a in by_anchor:
            rec=by_anchor[a]
            document.append('<p class="meta">Difficulty: '+to_html(rec[2],labels)+' · Type: '+to_html(rec[3],labels)+'<br>Status/version: '+to_html(rec[4],labels)+'</p>')
            if not html_links:
                document.append('<a href="'+CATALOGUE+'.pdf#nameddest='+a+'">Canonical catalogue entry</a>')
        document.append('<p>'+to_html(body,labels)+'</p></article>')
        if a in recency:
            fields=['Publication / issue date','Selected version / revision','Last verification','Evidence inspected','Version relationship / superseding source','Review policy']
            metadata='<details><summary>Version and verification record</summary><dl>'
            metadata+=''.join('<dt><strong>'+name+'</strong></dt><dd>'+to_html(value,labels)+'</dd>' for name,value in zip(fields,recency[a]))
            metadata+='</dl></details>'
            document[-1]=document[-1].replace('</article>',metadata+'</article>')
    document.append('<h2>Numbered source-link directory</h2>')
    for source_id,url in re.findall(r'^\\item\\hypertarget\{(source-\d+)\}\{\}\s*\\url\{([^}]+)\}',source,re.M):
        url=html.escape(web_url(url),quote=True)
        document.append('<p id="'+source_id+'"><a href="'+url+'">'+source_id+': '+url+'</a></p>')
    document.append('''<script>const search=document.getElementById('search'),articles=[...document.querySelectorAll('article')];function filter(){const q=search.value.toLowerCase();let n=0;articles.forEach(a=>{a.hidden=!a.textContent.toLowerCase().includes(q);if(!a.hidden)n++});document.getElementById('count').textContent=n+' notes';}search.addEventListener('input',filter);filter();</script></html>''')
    (ROOT/'catalogue_extended_notes.html').write_text('\n'.join(document))
    field_names=['publication','version','last_verified','evidence','supersession','review_policy']
    exported={}
    for a,values in recency.items():
        record={k:html.unescape(re.sub(r'<[^>]*>','',to_html(v,labels))) for k,v in zip(field_names,values)}
        verified=record['last_verified']
        match=re.match(r'^\d{4}-\d{2}-\d{2}',verified)
        record['verified_on']=match[0] if match else None
        record['verification_provenance']='new-source-inspection' if re.fullmatch(r'\d{4}-\d{2}-\d{2}',verified) else ('inherited-evidence' if match else 'not-established')
        record['source_urls']=list(dict.fromkeys(web_url(u) for u in re.findall(r'\\(?:href|url)\{(https?://[^}]+)\}',' '.join(by_anchor[a])+notes_by_id.get(a,''))))
        record['evidence_links']=list(dict.fromkeys(web_url(u) for u in re.findall(r'\\(?:href|url)\{([^}]+)\}',' '.join(values))))
        exported[a]=record
    (ROOT/'catalogue_recency.json').write_text(json.dumps({'schema_version':1,'source':CATALOGUE+'.tex','as_of':as_of,'entries':exported},ensure_ascii=False,indent=2)+'\n')
    print(f'Refreshed {route_summary}, {sum(len(r["required_readings"]) for r in routes+specialists)} selected readings, {len(notes)} extended notes and {len(recency)} recency records.')

if __name__=='__main__':refresh()
