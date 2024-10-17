##  Парсеры сайтов.

### Работа с зависимостями
* Устанавливаем `pip-compile`
```bash
pip install pip-tools
```
* Добавляем новую зависимость в список `project.dependencies` в `pyproject.toml`
* Генерируем обновленный `requirements.txt`
```bash
pip-compile -o requirements.txt pyproject.toml
```
* Устанавливаем зависимости
```bash
pip install -r requirements.txt
```

## Линтеры:

### pre-commit

1. Установить:
```shell
pip install pre-commit
```

2. Запустить скрипт:
```shell
pre-commit run -a
```
