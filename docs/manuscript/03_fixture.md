# Fixture observations

The fixture has five records and four distinct URL strings. With the limit disabled, all five records survive organization and JSON round-trip. The repeated URL appears twice in the fallback bucket with its two original titles. Its duplicated identity therefore remains visible to a downstream reader.

| Fixture title | Category | Reason |
|:--|:--|:--|
| Stone | Other | No category keyword matched |
| Exhibit | Technological | A tag supplies the keyword hardware |
| Education software | Social | Education and software score one each, and social is visited first |
| Shell | Other | No category keyword matched |
| Chair | Technological | The substring ai occurs within chair |

Setting the limit to two retains Stone and Exhibit. Their order matches the first two elements of the original JSON array. Running the unlimited case twice and writing both outputs with the repository's serializer produces the same bytes. The Chair case demonstrates why exact replay and topical validity are distinct questions. The fixture exercises a few specific branch conditions and supports no generalization about real-world distributions or accuracy.
