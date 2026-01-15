# 🚀 Инструкция по развертыванию обновления на сервере

## ✅ Что уже сделано локально

1. ✅ Все изменения протестированы локально
2. ✅ Коммит создан: `Fix events functionality: static events + 30-min alerts`
3. ✅ Изменения загружены на GitHub: https://github.com/byArto/crypto-analytics-bot

---

## 📋 Пошаговая инструкция для сервера

### Шаг 1: Подключиться к серверу по SSH

```bash
ssh your_user@your_server_ip
# Или используйте ваш способ подключения
```

---

### Шаг 2: Перейти в директорию с ботом

```bash
cd /path/to/crypto-analytics-bot
# Например: cd /home/user/crypto-analytics-bot
```

**Как узнать путь если забыли:**
```bash
# Найти процесс бота
ps aux | grep "python.*main.py"

# Или найти директорию по имени
find /home -name "crypto-analytics-bot" -type d 2>/dev/null
```

---

### Шаг 3: Остановить бота

**Вариант A: Если бот запущен через systemd**
```bash
sudo systemctl stop crypto-bot
# Или ваше имя сервиса
sudo systemctl stop telegram-bot
```

**Вариант B: Если бот запущен вручную**
```bash
# Найти процесс
ps aux | grep "python.*main.py"

# Убить процесс (используйте PID из вывода выше)
kill <PID>

# Или убить все процессы python main.py
pkill -f "python.*main.py"
```

**Проверка что бот остановлен:**
```bash
ps aux | grep "python.*main.py"
# Не должно быть запущенных процессов
```

---

### Шаг 4: Создать резервную копию (на всякий случай)

```bash
# Создать бэкап текущей версии
cp -r /path/to/crypto-analytics-bot /path/to/crypto-analytics-bot.backup.$(date +%Y%m%d-%H%M%S)

# Или только важные файлы
tar -czf ~/bot_backup_$(date +%Y%m%d-%H%M%S).tar.gz \
    modules/events.py \
    scheduler.py \
    i18n/ru.py \
    i18n/en.py \
    .env
```

---

### Шаг 5: Получить обновления с GitHub

```bash
# Убедитесь что вы в директории бота
pwd
# Должно быть: /path/to/crypto-analytics-bot

# Подтянуть изменения
git pull origin main
```

**Ожидаемый вывод:**
```
remote: Enumerating objects...
Receiving objects: 100%
Updating 614558a..833139b
Fast-forward
 .gitignore          |   6 ++
 EVENTS_UPDATE.md    | 390 ++++++++++++++++++++++++++++++++++++++++
 i18n/en.py          |  13 +-
 i18n/ru.py          |  13 +-
 modules/events.py   | 327 ++++++++++++++++++++++++++-------
 scheduler.py        |  19 ++
 6 files changed, 676 insertions(+), 109 deletions(-)
```

---

### Шаг 6: Проверить что обновления применились

```bash
# Проверить содержимое modules/events.py
head -20 modules/events.py

# Должны увидеть импорты: json, Path, aiohttp, timedelta
```

```bash
# Проверить scheduler.py
grep "check_event_alerts" scheduler.py

# Должна найтись функция check_event_alerts
```

---

### Шаг 7: Создать директорию для данных (если нужно)

```bash
# Создать папку data для хранения оповещений
mkdir -p data

# Установить права
chmod 755 data
```

---

### Шаг 8: Запустить бота обратно

**Вариант A: Через systemd**
```bash
sudo systemctl start crypto-bot
# Или ваше имя сервиса

# Проверить статус
sudo systemctl status crypto-bot

# Посмотреть логи
sudo journalctl -u crypto-bot -f
```

**Вариант B: Вручную**
```bash
# Активировать виртуальное окружение
source .venv/bin/activate

# Запустить в фоне с логами
nohup python main.py > bot.log 2>&1 &

# Или в screen/tmux
screen -S bot
python main.py
# Нажать Ctrl+A, затем D для отсоединения
```

---

### Шаг 9: Проверить что бот работает

```bash
# Проверить процесс
ps aux | grep "python.*main.py"

# Посмотреть логи
tail -f bot.log
# Или для systemd:
sudo journalctl -u crypto-bot -f
```

**Что должно быть в логах:**
```
⏰ Планировщик активен: проверка каждые 15 минут
INFO:apscheduler.scheduler:Scheduler started
INFO:apscheduler.scheduler:Added job "check_event_alerts" to job store "default"
```

---

### Шаг 10: Протестировать функцию /events в Telegram

1. Откройте бота в Telegram
2. Отправьте команду: `/events`
3. Должен появиться список актуальных событий:

**Ожидаемый ответ:**
```
📰 Важные рыночные события

Ниже перечислены события, которые могут повлиять на волатильность рынка.

🔴 US CPI Data Release
📅 2026-01-22 13:30 UTC
ℹ️ Consumer Price Index (inflation data) - typically causes market volatility.

🟠 Token Unlock: APT (Monthly)
📅 2026-01-25 12:00 UTC
ℹ️ Aptos token unlock - approximately 11.3M APT tokens unlocked monthly.

⏱ Обновлено: 14:30 UTC
```

---

### Шаг 11: Проверить работу 30-минутных оповещений

**Метод 1: Проверить логи через 5-10 минут**
```bash
# Смотрим логи планировщика
tail -f bot.log | grep "event"

# Или
sudo journalctl -u crypto-bot -f | grep "event"
```

**Что искать в логах:**
- Если есть события за 30 минут: `⚠️ Отправлено оповещение о событии за 30 минут`
- Если нет событий: просто тишина (это норма)

**Метод 2: Проверить файлы данных**
```bash
# Посмотреть файлы оповещений
ls -la data/

# Должны появиться файлы (если были оповещения):
# alerted_events.json
# alerted_30min_events.json

# Посмотреть содержимое
cat data/alerted_30min_events.json
```

---

## 🔧 Устранение проблем

### Проблема 1: Бот не запускается

**Решение:**
```bash
# Проверить зависимости
source .venv/bin/activate
pip install -r requirements.txt

# Проверить синтаксис
python -m py_compile modules/events.py
python -m py_compile scheduler.py
```

### Проблема 2: Команда /events не работает

**Решение:**
```bash
# Проверить логи на ошибки
tail -50 bot.log | grep -i error

# Запустить тест локально на сервере
python test_events_api.py

# Если теста нет, создать простую проверку:
python -c "
import asyncio
from modules.events import get_events

async def test():
    events = await get_events()
    print(f'События получены: {len(events)}')

asyncio.run(test())
"
```

### Проблема 3: 30-минутные оповещения не приходят

**Решение:**
```bash
# Проверить что планировщик запущен
grep "event_alerts_30min" bot.log

# Проверить настройки в .env
grep ALERT_CHAT_ID .env
grep ENABLE_AUTO_ALERTS .env

# Убедиться что ALERT_CHAT_ID настроен правильно
```

### Проблема 4: Git pull не работает

**Решение:**
```bash
# Проверить статус
git status

# Если есть локальные изменения, сохранить их
git stash

# Подтянуть изменения
git pull origin main

# Применить сохраненные изменения обратно (если нужно)
git stash pop
```

---

## 📊 Мониторинг после развертывания

### Первые 24 часа

**Проверяйте каждые 2-3 часа:**
```bash
# Статус процесса
ps aux | grep "python.*main.py"

# Логи за последние 10 минут
tail -50 bot.log

# Размер лога (не растет ли слишком быстро)
ls -lh bot.log
```

### Через неделю

**Проверьте:**
- ✅ Файлы data/*.json создались
- ✅ События обновляются корректно
- ✅ Пользователи получают актуальную информацию
- ✅ Нет ошибок в логах

---

## 📞 Если что-то пошло не так

### Быстрый откат к предыдущей версии

```bash
# Остановить бота
sudo systemctl stop crypto-bot
# Или: pkill -f "python.*main.py"

# Откатить изменения git
git reset --hard HEAD~1

# ИЛИ восстановить из бэкапа
rm -rf /path/to/crypto-analytics-bot
mv /path/to/crypto-analytics-bot.backup.YYYYMMDD-HHMMSS /path/to/crypto-analytics-bot

# Запустить бота
sudo systemctl start crypto-bot
```

---

## ✅ Контрольный чек-лист после развертывания

- [ ] Бот успешно запущен (процесс работает)
- [ ] Команда `/events` возвращает события
- [ ] События актуальные (даты в будущем)
- [ ] Планировщик активен (в логах видно "Планировщик активен")
- [ ] Папка `data/` создана
- [ ] Нет критических ошибок в логах
- [ ] Все остальные команды работают (/market, /volatility и т.д.)

---

## 📝 Полезные команды для администрирования

```bash
# Посмотреть версию коммита
git log --oneline -1

# Посмотреть изменения последнего коммита
git show HEAD

# Посмотреть статистику бота
echo "Запущен: $(ps aux | grep 'python.*main.py' | grep -v grep | wc -l) процесс(ов)"
echo "Размер логов: $(du -sh bot.log 2>/dev/null || echo 'нет логов')"
echo "Файлы данных: $(ls data/ 2>/dev/null | wc -l)"

# Очистить старые логи (если нужно)
truncate -s 0 bot.log
```

---

**Дата создания**: 2026-01-15
**Версия бота**: 2.0 (Events Module Refactored)
**GitHub**: https://github.com/byArto/crypto-analytics-bot
