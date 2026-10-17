-- Keep at least five words on the final line of a prose paragraph.
-- Each paragraph is first broken with its last five words tied together. If
-- that would overfill a line or stretch one beyond the normal tolerance, the
-- paragraph is broken normally instead. A width guard leaves very long
-- endings free.
local glyph = node.id('glyph')
local glue = node.id('glue')
local disc = node.id('disc')
local hlist = node.id('hlist')
local penalty = node.id('penalty')

local function tie_paragraph_ending(head)
  local current = node.tail(head)
  local boundaries = {}
  local discretionary = {}
  local has_word = false
  while current do
    if current.id == glyph or current.id == hlist then
      has_word = true
    elseif current.id == glue and (current.subtype == 13 or current.subtype == 14) then
      if has_word then
        boundaries[#boundaries + 1] = current
        if #boundaries == 5 then break end
        has_word = false
      end
    elseif current.id == disc then
      discretionary[#discretionary + 1] = current
    end
    current = current.prev
  end
  -- A genuinely short paragraph or list item should retain its natural length.
  if #boundaries < 5 then return head, false end
  local ending_width = node.dimensions(boundaries[5].next, node.tail(head))
  if ending_width > 0.8 * tex.hsize then return head, false end
  for i = 1, 4 do
    local mark = node.new(penalty)
    mark.penalty = 10000
    head = node.insert_before(head, boundaries[i], mark)
  end
  for _, hyphen in ipairs(discretionary) do
    hyphen.penalty = 10000
  end
  return head, true
end

-- Packing problems in a trial are recorded instead of reported; outside a
-- trial they are reported as TeX would.
local in_trial, trial_problem = false, false
local function report_quality(incident, detail, head, first, last)
  if in_trial then
    if incident == 'overfull' or incident == 'underfull' then trial_problem = true end
    return
  end
  local where = first == last and string.format(' detected at line %d', first)
    or string.format(' in paragraph at lines %d--%d', first, last)
  if incident == 'overfull' then
    texio.write_nl(string.format('Overfull \\hbox (%.5fpt too wide)', detail / 65536) .. where)
    if tex.overfullrule > 0 then
      local rule = node.new('rule')
      rule.width = tex.overfullrule
      return rule
    end
  elseif incident == 'underfull' then
    texio.write_nl(string.format('Underfull \\hbox (badness %d)', detail) .. where)
  elseif incident == 'tight' or incident == 'loose' then
    texio.write_nl(string.format('%s \\hbox (badness %d)', incident == 'tight' and 'Tight' or 'Loose', detail) .. where)
  end
end
luatexbase.add_to_callback('hpack_quality', report_quality, 'compendium.report_quality')

local function finish(lines, info)
  local nest = tex.nest[tex.nest.ptr]
  nest.prevdepth = info.prevdepth
  nest.prevgraf = info.prevgraf
  return lines
end

local function break_paragraph(head)
  local trial, tied = tie_paragraph_ending(node.copy_list(head))
  if not tied then
    node.flush_list(trial)
    return finish(tex.linebreak(head))
  end
  -- A trial line looser than the normal tolerance counts as a problem, so the
  -- rule never buys a long last line with visibly stretched spacing.
  local hbadness = tex.hbadness
  tex.hbadness = tex.tolerance
  in_trial, trial_problem = true, false
  local lines, info = tex.linebreak(trial)
  in_trial = false
  tex.hbadness = hbadness
  if not trial_problem then
    node.flush_list(head)
    return finish(lines, info)
  end
  node.flush_list(lines)
  return finish(tex.linebreak(head))
end

luatexbase.add_to_callback('linebreak_filter', break_paragraph,
                          'compendium.tie_paragraph_ending')
