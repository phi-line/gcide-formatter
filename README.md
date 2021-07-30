# gcide-formatter

Convert the GNU Collaborative International Dictionary of English to an SQLite database.

## How to use

1. `pip install beautifulsoup4`
1. Download the latest version of [GCIDE_XML](http://www.ibiblio.org/webster/)
2. Extract the archive and move the containing xml_files directory here
3. Run `./gcide_sqlite.py`

```shell
pip install beautifulsoup4
curl http://www.ibiblio.org/webster/gcide_xml-0.51.zip
unzip gcide_xml-0.51.zip
mv gcide_xml-0.51/xml_files gcide-formatter
./gcide_sqlite.py
```