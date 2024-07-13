# Wstęp

Celem projektu jest przygotowanie aplikacji, która będzie zapisywać logi z serwera do bazy danych (TimescaleDB).
Następnie dostarczy zgrupowane informacje do interfejsu użytkownika (frontend), gdzie zostaną one przedstawione w postaci wykresu.

# Opis aplikacji

## Odczyt logów

Logi będą zapisane w pliku `server.log`. Logi są dopisywane cyklicznie, poajwiają się nowe wiersze co jakiś czas.

Logi mają format:

        INFO 2024-04-24 03:29:30,429 manufaktur.projects.models.models:480 basket_item BasketItem for project: 8163c80360ec32be3fc6e6c30203b32d does not exist
        DEBUG 2024-04-24 07:14:59,285 manufaktur.utils.views.helpers.helpers:68 run Can't match url /static.php/ to any products and categories
        WARNING 2024-04-24 07:32:52,439 manufaktur.products.models.managers.product_category.product_category:72 get_for_url ProductCategory does not exist for specified path: /contura/Holz/5000003640.html/. Details: 'tree_path'
        ...

- Aplikacja odczytuje plik i zapisuje wiersze do bazy danych, dzielać na odpowiednie kolumny
- Aplikacja potrafi parsować logi wg zdefiniowanego formatu (użytkonik powinien mieć możliwosć określenia tego patternu) i wydzielić informacje z logu takie jak: time, level (INFO, DEBUG, CRITICAL, WARNING, ERROR), text message
- Aplikacja wykrywa, że pojawiły się nowe logi w pliku i dodaje je do bazy danych.

## RestApi

- Aplikacja posiada podstawowy interfejs api (django rest framework) który umożliwia zwracania podstawowych informacji na temat logów

## Frontend

Prosty interfejs w formie strony która wyświetla wykres i wizualizuje dane.

Strona poza wykresem umozliwia zmianę zakresu danych które są wyświetlane tj. zmiana zakresu logów, wybór typu logów, filtrowanie, wyświetlanie zagregowanych danych.


- Istnieje możliwość filtorwania logów w zadanym zakresie czasowym (od do)
- Istnieje możliwosć filtorwania logów tylko dla wybranych typów: INFO, DEBUG, CRITICAL
- Istnieje możliwość agregowania logów dla wybranej roździelczosci, np ile wystapiło logów typu debug w ciagu roku, miesiaca, tygodnia, dnia, godziny
- Istnieje możliwosć filtorwania logów po wpisaniu prostego zapytania -> "text message zawiera"

Zachęcmy do wykorzystania HTMX:

HTMX  https://htmx.org/
Django-htmx https://django-htmx.readthedocs.io/en/latest/changelog.html

### HTMX Resources (eng)

### Playgrounds

HTMX might be new to the candidate. Therefore we provide a couple of interesting links about this technology.

- https://github.com/lassebomh/htmx-playground?tab=readme-ov-file
- https://lassebomh.github.io/htmx-playground/?url=.%252Fplaygrounds%252Fclicktoedit%252F.playground.json


### HTMX and Django

- https://adamj.eu/tech/2022/03/02/django-htmx-on-read-the-docs/
- https://django-htmx.readthedocs.io/en/latest/changelog.html


### Tutorials

- https://refine.dev/blog/what-is-htmx/ - probably best tutorial available as for 03.2024
- https://www.photondesigner.com/articles/database-search-django-htmx


### Videotutorials

- https://www.youtube.com/watch?v=cpzowDDJj24&feature=youtu.be
- https://www.youtube.com/watch?v=Ula0c_rZ6gk&list=PL-2EBeDYMIbRByZ8GXhcnQSuv2dog4JxY 


# Wymagania

* podział na zadania (github issues) i tworzenie pull requestów do tych zadań;
* pierwszy pull request powinien zawierać tylko szkielet projektu, bez żadnych ficzerów (np. bootstrap z createapp)
* Backend: Django, Timescaledb
* Frontend: można wykorzystać bootstrap do szybkiego stylowania, chartjs

# Co będzie brane pod uwagę:

- Przede wszystkim proces powstawania projektu
- Funkcjonalność
- Szybkość działania aplikacji
- Testy - kilka testów jednostkowych, sprawdzających poprawność np parsowania logów
- *Czytelne README.md wyjaśniające co robi projekt i jak go uruchomić - po angielsku*
- Commity oraz cały kod po angielsku

# Zasoby

* https://www.timescale.com/blog/getting-sensor-data-into-timescaledb-via-django/
* https://docs.timescale.com/