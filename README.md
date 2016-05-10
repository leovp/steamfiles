# steamfiles
Python library for parsing the most common Steam file formats.  
The library has a familiar JSON-like interface: ```load()``` / ```loads()``` for loading the data,  
and ```dump()``` / ```dumps()``` for saving the data back to the file.

## Format support
|             | Read  | Write |
| ----------- | :---: | :---: |
| ACF         | ✅ | ✅ |
| appinfo.vdf | ✅ | ✅ |
| Manifest    | ✅ | ✅ |

## Quickstart

```steamfiles``` requires Python 3.3+

Install the latest stable version:

    pip install steamfiles

## License

steamfiles is distributed under the terms of the MIT license.

See [LICENSE](LICENSE) file for all the details.
