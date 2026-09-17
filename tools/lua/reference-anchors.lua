-- Las anclas bibliográficas vacías son destinos, no títulos del índice.
-- Un Span conserva el identificador en PDF/EPUB sin crear una sección vacía.
return {{Header = function(header)
  if header.identifier:match('^ref%-') and #header.content == 0 then
    return pandoc.Plain({pandoc.Span({}, header.attr)})
  end
end}}
