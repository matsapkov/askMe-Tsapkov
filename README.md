# AskMe_Tsapkov

Репозиторий проекта **AskMe** — учебного проекта курса первого семестра [Технопарка ВК](https://park.vk.company/) по направлению *Веб-разработка*.

Этот проект представляет собой форум вопросов и ответов, реализованный на Django.

📦 Репозиторий с вёрсткой: [askme-layout](https://github.com/matsapkov/askMe-frontend)  

📂 Фикстура с дампом базы данных: [Google Drive](https://drive.google.com/drive/folders/13Jxy7OxXk1trmOsZVCIwv1Jab77_XkFM?usp=drive_link)

---

## Загрузка данных из фикстуры

Чтобы загрузить фикстуру в базу данных, выполните следующие шаги:

1. Перейдите в корневую директорию проекта:
   ```cmd
      cd путь/до/репозитория
2. Перейдите в директорию *app* и создайте папку *fixtures*
    ```cmd
      cd путь/до/репозитория
3. Скопируйте загруженный JSON-файл в эту папку и выполните команду:
    ```cmd
      python manage.py loaddata app/fixtures/fixtures.json
