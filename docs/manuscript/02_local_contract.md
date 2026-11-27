# Organization and serialization

The loader reads UTF-8 JSON using Python's standard library [@python-json]. If the configured maximum is positive and smaller than the number of entries, it retains the initial segment of the array. The default limit is 40. A nonpositive limit leaves the loaded array intact.

For each record, the organizer joins the URL, title, description, and tags with spaces and lowercases the result. Each distinct keyword in a category contributes one point if present anywhere in the resulting string. The highest positive score wins. The implementation visits the political, economic, social, and technological categories in that order and replaces the selected category only when it encounters a strictly larger score. A record with no match enters the fallback category, named `other` in the serialized file.

The organizer appends the original records in input order within their assigned buckets. It creates a JSON object with one array per category, including empty arrays. Repeated URLs remain present as separate records, preserving each record's original metadata. Key and row order are properties of this implementation and the fixed fixture, so a consumer that needs source array order across multiple buckets should preserve its own position identifiers.
