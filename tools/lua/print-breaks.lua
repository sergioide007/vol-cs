-- Cortes tipográficos exclusivos del PDF; conserva el texto del manuscrito.
-- \hspace{0pt} permite a TeX dividir la primera palabra de una celda.
if not FORMAT:match('latex') then return {} end

local function latex_inline(inline)
  return pandoc.write(pandoc.Pandoc({pandoc.Plain({inline})}), 'latex')
end

local function cell_word(word)
  local text = latex_inline(word)
  text = text:gsub('/', '/\\allowbreak{}')
  text = text:gsub('→', '→\\allowbreak{}')
  text = text:gsub('([a-z])([A-Z])', '%1\\allowbreak{}%2')
  return pandoc.RawInline('latex', '\\hspace{0pt}' .. text)
end

local function code_breaks(code)
  -- Pandoc hace el escapado; solo añadimos cortes en caracteres seguros.
  local text = latex_inline(code)
  text = text:gsub('%.', '.\\allowbreak{}')
  text = text:gsub('/', '/\\allowbreak{}')
  text = text:gsub('([a-z])([A-Z])', '%1\\allowbreak{}%2')
  if code.text == 'infrastructure/' then
    text = text:gsub('infrastructure', 'infra\\allowbreak{}structure')
  end
  return pandoc.RawInline('latex', text)
end

return {{Table = function(tbl)
  return tbl:walk({Str = cell_word, Code = code_breaks})
end}}
