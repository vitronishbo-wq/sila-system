name: code-quality
steps:
  - run: flake8 .              # valida estilo e qualidade do código Python
  - run: mypy .                # checa tipos e módulos incompletos
  - run: pylint apps/          # análise mais profunda de arquitetura
  - run: python -m compileall . # checa erros de sintaxe
  - notify: "Validação concluída. Corrige os pontos indicados."
