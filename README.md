# Japanese Database (JD)

[Japanese Database: Live Link](https://jd.exomut.com)

**JD** is a Django based Japanese dictionary for retrieving definitions quickly using Ajax and JQuery. The dictionary file is using [JMDict](http://ftp.monash.edu/pub/nihongo/00INDEX.html#dic_fil).

As of now, searches are done in all directions for words containing the search term; Kanji, Katakana, English.


## Roadmap

Ordered by priority.

- [x] JMDict xml file to SQLite parsing.
- [x] Ajax pagination for large results.

- [x] Add search customizations:
  - [x] Search parts: Starts With, Ends With, Contains, Full Match.
- [x] More information about the definition, such as grammar type.
- [x] Add the Tatoeba example sentence dictionary.
- [ ] Improve the design.
- [ ] Romaji support.
- [x] Put on production server for public use.
- [ ] User Login to allow saving words.
  - [ ] Exporting saved words.
- [ ] Kanji Lookup and information.
- [ ] Include other languages; Russian, French...

### Rebuilding the JMDict Database and Running Locally

Since Github does not allow files over 100MB the database must be built after downloading.

```bash
python manage.py migrate
```
If JMDict needs to be updated, download the new [JMDict](http://ftp.monash.edu/pub/nihongo/00INDEX.html#dic_fil) and replace the old one in the assets folder without extracting it.

Run the following command to parse the dictionary in to the database. The dictionary is very large, so this may take a few minutes.

```bash
python manage.py rebuild_jmdict_db
python manage.py rebuild_examples
```
Warning: All entries will be removed from the dictionary table before rebuilding.

```bash
python manage.py runserver
```
Use the link provided by the server in a browser to run Japanese Database.

