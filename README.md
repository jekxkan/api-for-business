Приложение, разработанное для помощи бизнесу в аналитике.
Поддерживаемый функционал:
- регистрация пользователя(добавляем запись в бд)
- аналитика (ср.возраст пользователей, их соотношение полов и т.д)

Порядок производимых действий: приходит post- или get-запрос от API (router.py), далее производим соответствующее действие в бд (service.py) и возращаем результат