#!/usr/bin/env bash
# release.sh — Обновить версию, сгенерировать журнал изменений, создать тег и отправить.
# Использование: ./scripts/release.sh patch|minor|major
set -euo pipefail

TIP_OBNOVLENIYA="${1:?Использование: $0 patch|minor|major}"

# Убедиться, что рабочее дерево чистое
if [[ -n "$(git status --porcelain)" ]]; then
    echo "ОШИБКА: Рабочий каталог не чистый. Сделайте коммит или stash изменений."
    exit 1
fi

# Убедиться, что мы на ветке main
VETKA=$(git rev-parse --abbrev-ref HEAD)
if [[ "$VETKA" != "main" ]]; then
    echo "ОШИБКА: Необходимо быть на ветке 'main' (сейчас на '$VETKA')."
    exit 1
fi

# Обновить версию
uv version --bump "$TIP_OBNOVLENIYA"
NOVAYA_VERSIYA=$(uv version)
echo "==> Версия обновлена до v$NOVAYA_VERSIYA"

# Сгенерировать журнал изменений (если git-cliff доступен)
if command -v git-cliff &>/dev/null; then
    git-cliff --tag "v$NOVAYA_VERSIYA" -o CHANGELOG.md
    echo "==> CHANGELOG.md сгенерирован"
    FAYLY_CHANGELOG="CHANGELOG.md"
else
    echo "==> git-cliff не найден, пропуск генерации журнала изменений"
    echo "    Установите: brew install git-cliff"
    FAYLY_CHANGELOG=""
fi

# Коммит обновления версии + журнал изменений
git add pyproject.toml uv.lock $FAYLY_CHANGELOG
git commit -m "chore(release): v$NOVAYA_VERSIYA"

# Создать аннотированный тег
git tag -a "v$NOVAYA_VERSIYA" -m "Релиз v$NOVAYA_VERSIYA"

echo "==> Создан тег v$NOVAYA_VERSIYA"
echo ""
echo "Готово к отправке. Выполните:"
echo "  git push origin main --follow-tags"
echo ""
echo "Или для публикации на PyPI:"
echo "  git push origin main --follow-tags && uv build && uv publish"
