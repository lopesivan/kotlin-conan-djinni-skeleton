# Projeto 01 — primeira chamada C++ via Djinni

Este exemplo demonstra o caminho minimo:

```text
MainActivity.kt
  -> NativeApi.java (gerado)
  -> JNI (gerado)
  -> NativeApi.cpp
  -> String exibida pelo Compose
```

O contrato fica em `projeto/djinni/native_api.djinni`. Os arquivos Java, JNI
e C++ gerados ficam em `examples/01-projeto/build/generated/djinni/` e nao
sao versionados.

## Executar

```bash
cd examples/01-projeto
make run
```

Na primeira execucao, Conan instala `djinni-generator/1.4.0` e o script baixa
uma revisao fixada de `djinni-support-lib` para o diretorio `build/`.

A tela deve mostrar:

```text
Hello from C++ via Djinni
```
