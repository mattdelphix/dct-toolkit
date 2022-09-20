# dct-toolkit

## What is it

dct-toolkit is a set of scripts, which are delivered by Delphix professional services team.
dct-toolkit scripts look and feel like UNIX executables, following the typical conventions of using flags for arguments.  
dct-toolkit is written in Python, but no knowledge of Python is required unless you want to extend it.  In fact, no programming experience whatsoever is required to use the dct-toolkit.

## What's new

Please check a [change log](https://github.com/delphix/dct-oolkit/blob/master/CHANGELOG.md) for list of changes.

## How to get started
### Compiled version

Download a compiled version of dct-toolkit for required platform from a [releases  page](https://github.com/delphix/dct-toolkit/releases).
Create a configuration file *dct-tools.conf* based on dct-tools.conf.example or a Wiki page.

Check a [documentation](https://github.com/delphix/dct-toolkit/wiki) for more details



### Source version

Python 3.9 or higher

**Required packages**
- tabulate
- pandas
- requests
- urllib3


### Known issues

No known issues at the moment.

### Support matrix

New releases of dct-toolkit are tested with Delphix Data Control Tower versions, which are in primary or extended support.
Ex. 1.0 release was tested with version 2.1.0 Delphix Data Control tower.

dct-toolkit is designed to support many versions of Delphix Engines, although if a new version is released after dct-toolkit release
it may stop working due to API changes. To mitigate this issue until next dct-toolkit version will be release, please add
-dever parameter to your commands with the following values:

|dct-toolkit   |Delphix DCT version   |API version |
| :---         |     :---:            | :---       |
| 1.0.0        | Delphix DCT 2.1.0    | API 1.11.11|




## <a id="contribute"></a>Contribute

1.  Fork the project.
2.  Make your bug fix or new feature.
3.  Add tests for your code.
4.  Send a pull request.

Contributions must be signed as `User Name <user@email.com>`. Make sure to [set up Git with user name and email address](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup). Bug fixes should branch from the current stable branch. New features should be based on the `master` branch.

#### <a id="code-of-conduct"></a>Code of Conduct

This project operates under the [Delphix Code of Conduct](https://delphix.github.io/code-of-conduct.html). By participating in this project you agree to abide by its terms.

#### <a id="contributor-agreement"></a>Contributor Agreement

All contributors are required to sign the Delphix Contributor agreement prior to contributing code to an open source repository. This process is handled automatically by [cla-assistant](https://cla-assistant.io/). Simply open a pull request and a bot will automatically check to see if you have signed the latest agreement. If not, you will be prompted to do so as part of the pull request process.


## <a id="reporting_issues"></a>Reporting Issues

Issues should be reported in the GitHub repo's issue tab. Include a link to it.

## <a id="statement-of-support"></a>Statement of Support

This software is provided as-is, without warranty of any kind or commercial support through Delphix. See the associated license for additional details. Questions, issues, feature requests, and contributions should be directed to the community as outlined in the [Delphix Community Guidelines](https://delphix.github.io/community-guidelines.html).


## <a id="license"></a>License
```
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
```
Copyright (c) 2022 by Delphix. All rights reserved.
