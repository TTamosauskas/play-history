# CI e publicação

O workflow `static.yml` valida build, JavaScript, busca por ano e integridade curatorial.

A publicação pública é feita exclusivamente pelo GitHub Pages nativo a partir da branch `main`. Manter um único caminho de deploy evita concorrência entre o artefato `_site` de validação e a raiz efetivamente servida pelo Pages.
