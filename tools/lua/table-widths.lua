-- ===========================================================================
-- Código Sintético — filtro Lua: anchos de columna de tabla
-- Motivo: pandoc genera tablas con anchos naturales (o sin ancho) que en la
-- caja de texto de 6x9 (4,5 pulgadas) desbordan hacia la guillotina. Este
-- filtro asigna un ancho relativo igual a cada columna, de modo que LaTeX
-- emita columnas del tipo p{...} (con ajuste de línea) y el EPUB ajuste el
-- texto a la pantalla.
-- Uso: pandoc --lua-filter=tools/lua/table-widths.lua
-- Compatibilidad: pandoc 2.x (ColWidth como constructor) y pandoc 3.x
-- (el ancho es directamente un número).
-- ===========================================================================

-- Devuelve el valor de ancho adecuado a la versión de pandoc en uso.
local function width_value(w)
  if pandoc.ColWidth ~= nil and type(pandoc.ColWidth) == "table"
     and pandoc.ColWidth.ColWidth ~= nil then
    return pandoc.ColWidth.ColWidth(w)          -- pandoc 2.x
  end
  return w                                       -- pandoc 3.x: número 0..1
end

local function set_widths(tbl)
  local n = #tbl.colspecs
  if n == 0 then
    return tbl
  end

  local each = 0.98 / n                          -- margen de seguridad del 2 %
  local specs = pandoc.List()
  local widths = pandoc.List()

  for i = 1, n do
    local align = tbl.colspecs[i][1]
    specs:insert({ align, width_value(each) })
    widths:insert(each)
  end

  tbl.colspecs = specs

  -- Sincroniza el campo `width` cuando la versión de pandoc lo expone.
  pcall(function()
    if tbl.width ~= nil then
      tbl.width = widths
    end
  end)

  return tbl
end

function Table(tbl)
  return set_widths(tbl)
end