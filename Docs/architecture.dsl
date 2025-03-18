workspace {

model {
    ClusterActivityMonitor = softwareSystem "Монитор кластеров" "Устройство для показывания активности на этаже" {
        masterService = container "Master" "Raspberry PI, связывающий все. Обрабатывает основные функции системы." "Server-side Application"
        database = container "База данных" "SQLite, для сохранения информации о пользователях, чтобы постоянно не обращаться к API платформы" "Database"
        slaveService = container "Slaves" "Сервис взаимодействия с STM32. Управляет выводом информации и проверкой модулей" "Server-side Application"
        peerService = container "Сервис проверки информации занятого места" "Проверяет БД. Если нет записи в БД - стучится к schoolAPI" "Server-side Application"
        prometheusService = container "Сервис проверки занятых мест" "Получает информацию о занятых местах" "Server-side Application"
    }

    slaveSTM32 = softwareSystem "STM32" "Модули, подключенные к светодиодам и выводящие информацию на них"
    schoolAPI = softwareSystem "API платформы" "Необходим для проверки трайба пира"
    grafometheus = softwareSystem "msk.grafometheus (prometheus)" "API для получения инфо о занятых местах"
    
    masterService -> slaveService "Отправление данных о цвете светодиодов"
    slaveService -> slaveSTM32 "I2C"
    masterService -> prometheusService "Использует"
    prometheusService -> grafometheus "Получает информацию"
    masterService -> peerService "Получает цвет, основываясь на нике пира от grafometheus"
    peerService -> database "Проверяет, есть ли запись о трайбе в БД"
    peerService -> schoolAPI "Если записи нет, стучится до API платформы и сохраняет запись"
}

views {    
  
    container ClusterActivityMonitor {
        include *
        include slaveSTM32
        include schoolAPI
        include grafometheus
        autolayout lr
    }
    
    theme default
}
}
