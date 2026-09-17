# Kotlin + Conan + Djinni

Esqueleto de projeto Android Kotlin-first. A interface, o estado e a navegacao
ficam em Kotlin/Compose. Conan empacota codigo C++ proprio ou externo, e Djinni
gera somente a fronteira necessaria entre Kotlin/Java, JNI e C++.

## Estrutura

```text
gradle/libs.versions.toml  catalogo central de versoes
projeto/recipes/           receitas Conan 2
projeto/djinni/            contratos Djinni
modulos/                   bibliotecas C++ proprias (adicione aqui)
third_party/               fontes externas (adicione aqui)
examples/01-projeto/       aplicativo Kotlin/Compose
examples/02-projeto/       aplicativo Kotlin/Compose
examples/03-projeto/       aplicativo Kotlin/Compose
```

## Primeiros comandos

Crie `local.properties` apontando para o Android SDK:

```properties
sdk.dir=/caminho/para/Android/Sdk
```

Se o `gradle-wrapper.jar` ainda nao existir, gere-o uma vez com um Gradle
instalado no sistema:

```bash
gradle wrapper
```

Depois, os aplicativos podem ser tratados separadamente:

```bash
./gradlew :examples:01-projeto:assembleDebug
./gradlew :examples:02-projeto:assembleDebug
./gradlew :examples:03-projeto:assembleDebug
```

Para gerar a fronteira de exemplo com um executavel `djinni` instalado:

```bash
./gradlew generateDjinni
```

A saida fica em `build/generated/djinni/` e nao e versionada. A geracao Djinni
nao participa automaticamente da compilacao Android ate que um modulo C++ seja
adicionado e conectado ao aplicativo.

## Regra arquitetural

Os aplicativos em `examples/NN-projeto` nao compilam diretamente o conteudo de
`third_party/`. Uma biblioteca nativa deve ser empacotada por uma receita Conan
e exposta ao Kotlin por um contrato pequeno em `projeto/djinni/`.

