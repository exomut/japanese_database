# Japanese Database (JD)

**JD** is a Django based Japanese dictionary for retrieving definitions quickly using Ajax and JQuery. The dictionary file is using [JMDict](http://ftp.monash.edu/pub/nihongo/00INDEX.html#dic_fil).

As of now, searches are done in all directions for words containing the search term; Kanji, Katakana, English.

## Running JD

I plan on putting JD on a production server once development has progressed more. For now download the project and use the following command to run a test server. Open your browser using the link provided by the run server command.

```bash
python manage.py runserver
```

## Roadmap

Ordered by priority.

- [x] JMDict xml file to SQLite parsing.
- [x] Ajax pagination for large results.

- [ ] Add search customizations:
  - [ ] Look up direction.
  - [ ] Search parts: Starts With, Ends With, Contains, Full Match.
- [ ] More information about the definition, such as grammar type.
- [ ] Add the Tatoeba example sentence dictionary.
- [ ] Improve the design.
- [ ] Romaji support.
- [ ] Put on production server for public use.
- [ ] User Login to allow saving words.
  - [ ] Exporting saved words.
- [ ] Kanji Lookup and information.
- [ ] Include other languages; Russian, French...

### Rebuilt the JMdict Database

Since Github does not allow files over 100MB the database must be built after downloading.

```bash
python manage.py migrate
```

If JMDict needs to be updated, download the new [JMDict](http://ftp.monash.edu/pub/nihongo/00INDEX.html#dic_fil) and replace the old one in the assets folder without extracting it.

Run the following command to parse the dictionary in to the database. The dictionary is very large, so this may take a few minutes.

```bash
python manage.py rebuild_jmdict_db
```

Warning: All entries will be removed from the dictionary table before rebuilding.
