-- Discourage fewer than five words on the final line of a prose paragraph.
-- Soft penalties and a width guard preserve flexibility around technical text.
local glyph = node.id('glyph')
local glue = node.id('glue')
local disc = node.id('disc')
local hlist = node.id('hlist')
local penalty = node.id('penalty')

local function balance_paragraph_ending(head)
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
  if #boundaries < 5 then return head end
  local ending_width = node.dimensions(boundaries[5].next, node.tail(head))
  if ending_width > 0.35 * tex.hsize then return head end
  for i = 1, 4 do
    local mark = node.new(penalty)
    mark.penalty = 5000
    head = node.insert_before(head, boundaries[i], mark)
  end
  for _, hyphen in ipairs(discretionary) do
    hyphen.penalty = 5000
  end
  return head
end

luatexbase.add_to_callback('pre_linebreak_filter', balance_paragraph_ending,
                          'compendium.balance_paragraph_ending')
