# Receitas Conan 2

Crie uma subpasta por pacote:

```text
projeto/recipes/minha-biblioteca/conanfile.py
```

Cada receita deve exportar os fontes necessarios de `modulos/` ou
`third_party/`, compilar o pacote e publicar os metadados CMake em
`package_info()`.

