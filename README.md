# SlavesBotVK - бот для игры "ВРабстве 3" ВКонтакте.

Скрипт бота для игры ВРабстве (Рабы 3.0) ВКонтакте, для начала работы нужно ввести токен игры и выбрать интересующие вас функции. 
Как получить токен игры?
Расскажу на примере браузера Google Chrome
1. Запускаем мини-игру ВРабстве (https://vk.com/app7790408)
2. Кликаем правой кнопкой мыши и выбираем "Просмотреть код" (Ctrl + Shift + I)
3. Переходим в раздел Network после чего обновляем приложение
4. После обновления игра начнёт обмен пакетами, ищим в списке пакет с именем "me" и кликаем на него
5. Переходим в подраздел Headers, пролистываем вниз и находим строку "authorization: Bearer " копируя всё что написано после слова Bearer в переменную token в файле SlavesBotVK.py
6. Проверяем, совпадают ли строки из переменных Origin, Referer, UserAgent со строками из пакета 'me' в браузере с игрой
7. Переходим к настройке опций бота, они находятся сразу за комментарием #Settings
   1. UpgradeLimited - диапазон прибыли рабов в котором будет работать автоматическое улучшение
   2. MaxProfit - Максимальный доход раба, при котором ещё возможна его покупка
   3. CheckInApp - Выполнение проверки входа пользователя в приложение
   4. Act_GetBonus - Функция автоматической сборки бонусов
   5. Act_UpgradeSlaves - Функция автоматеческого улучшения рабов
   6. Act_DeleteNoWalidSlaves - Функция удаления невыгодных для улучшения рабов
   7. Act_FetterSlaves - Функция автоматической установки оков рабам
   8. Act_BuyTop - Функция выкупа рабов у Топа по монетам
   9. Act_RestoringSlaves - Функция восстановления потеряных рабов
   10. SkipDisabledTasks - Функция пропуска пакетов не выбраных в настройках

В боте реализован диспетчер пакетов который поочерёдно выполняет все действия, что сводит к минимому возможность блокировки аккаунта независимо от количества активных опций, так же это даёт возможность ставить действия в очередь, то есть если у вас недостаточный баланс для выполнения того или иного действия(покупки какого-то раба или улучшения его) этот пакет будет временно пропущен пока не будет накоплена нужная сумма. Так же бот фиксирует всех приобретённых рабов за период его работы, то есть появляется возможность быстро восстановиться в случае если ваших рабов выкупят, ведь все их ID сохраняются в папке. 

Тесты:
За 3 часа работы доход был увеличен с 200 до 2400, а количество рабов с 25 до 400. Бот хорошо автономно распоряжается заработаными деньгами и очень быстро развивает аккаунт.
Вы можете активировать все опции, загрузить бота на сервер и забыть о нём или запустить его на персональном компьютере, так же есть поддержка и смартфонов, но требуется установка Termux. К тому же, при запуске всех опций, аккаунт не выводится в топ, что уменьшает вероятность выкупа всех ваших рабов. Если хотите выйти в топ, то дайте время поработать боту во всю, а затем оставте только установку оков.

Для запуска на Android в Termux нужно ввести сдедущие команды
   1. pkg update && pkg upgrade -y
   2. pkg install python git nano
   3. pip install requests
   4. git clone https://github.com/Seffel2274/SlavesBotVK
   5. cd SlavesBotVK
   6. nano SlavesBotVK.py
   7. Редактируем настройки и сохраняем файл
   8. python SlavesBotVK.py
   9. Готово

p.s. Проверил скрипт на второй страничке где ни разу не использовалось приложение. Итог: За 2 часа прибыль стала 500 монет/мин, количество рабов упёрлось в 100, скоро реализую автоматическое расширение помещения при заполнении, а так же приоритеты в менеджере заданий. На основном аккаунте прибыль перевалила за 5000 монет/мин. количество рабов 900.
Если хотите в очень короткие сроки прокачать аккаунт, выбирайте именно мой скрипт. Буду рад если кликните на звёздочку и предложите какой либо новый проект: https://vk.com/seffeloff

Если у кого-то есть возможность поддержать развитие дальнейших проектов выможете сделать мне приятно и подкинуть на кофеёк рублик по этим реквизитам:
*** СберБанк:     5469 3300 1216 5142 ***
*** ВТБ:          2200 2407 6106 0587 ***

#Бот для рабов ВК
#Рабы 3.0 Ввк бот
#Бот на Рабство ВК
