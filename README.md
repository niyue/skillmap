# skillmap
A tool for generating skill map/tree like diagram.

# What is a skill map/tree?
Skill tree is a term used in video games, and it can be used for describing roadmaps for software project development as well.

This project borrows inspiration and ideas from two sources:
1. https://hacks.mozilla.org/2018/10/webassemblys-post-mvp-future/
2. https://github.com/nikomatsakis/skill-tree

# Installation
```
pip install skillmap
```
After installation, a `skillmap` command is available.

# Usage
1. Create a toml format skill map descriptor file. You can find more details about this descriptor format [here](docs/skillmap_descriptor.md). For a minimal example, see [`docs/examples/hello_world.toml`](docs/examples/hello_world.toml)
```
[skillmap]
name = "hello world"
icon = "bicycle"

[groups.learn_python]
name = "learn python"
icon = "rocket"
    [groups.learn_python.skills.print]
    name = "print statement"
    icon = "printer"
    [groups.learn_python.skills.string]
    name = "string literal"
    icon = "book"
```

2. Run `skillmap path/to/your/skillmap.toml`
   1. For example, `skillmap docs/examples/hello_world.toml`
3. Copy the generated skill map diagram to your clipboard.
4. Paste the diagram to a mermaid diagram editor, for example, [`https://mermaid-js.github.io/mermaid-live-editor`](https://mermaid-js.github.io/mermaid-live-editor).

# Examples
```mermaid
flowchart TD
url_shortener(fa:fa-hashtag <br/>url shortener)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.webui[fa:fa-desktop web ui]
groups.webui.skills.url_validator(fa:fa-globe <br/>url validator)
class groups.webui.skills.url_validator newSkill;
groups.webui.skills.react-->groups.webui.skills.url_validator
groups.webui.skills.react(fa:fa-list <br/>react)
class groups.webui.skills.react beingLearnedSkill;

end
class groups.webui normalSkillGroup;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.native_client[fa:fa-desktop native client]
groups.native_client.skills.react_native(fa:fa-mobile <br/>react native)
class groups.native_client.skills.react_native newSkill;

groups.native_client.skills.other_clients(fa:fa-lock <br/>???)
class groups.native_client.skills.other_clients unknownSkill;

end
class groups.native_client newSkillGroup;
groups.webui-->groups.native_client

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.backend[fa:fa-server backend]
groups.backend.skills.restapi(fa:fa-send <br/>REST API)
class groups.backend.skills.restapi learnedSkill;

groups.backend.skills.database(fa:fa-database <br/>database)
class groups.backend.skills.database learnedSkill;

end
class groups.backend normalSkillGroup;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.partitioned_backend[fa:fa-copy partitioned backend]
groups.partitioned_backend.skills.proxy(fa:fa-anchor <br/>proxy)
class groups.partitioned_backend.skills.proxy beingLearnedSkill;

groups.partitioned_backend.skills.database(fa:fa-database <br/>partitioned database)
class groups.partitioned_backend.skills.database beingLearnedSkill;

end
class groups.partitioned_backend normalSkillGroup;
groups.backend-->groups.partitioned_backend

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.cache[ cache]
groups.cache.skills.memcache(fa:fa-magnet <br/>memcache)
class groups.cache.skills.memcache learnedSkill;

groups.cache.skills.redis(fa:fa-lock <br/>???)
class groups.cache.skills.redis unknownSkill;

end
class groups.cache normalSkillGroup;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
url_shortener-->groups.webui
url_shortener-->groups.backend
url_shortener-->groups.cache
classDef normalSkillGroup stroke:#0096C7,stroke-width:4px,fill:#CAF0F8;

classDef beingLearnedSkill stroke-width:2px,stroke:#90E0EF,fill:#ADE8F4;
classDef learnedSkill stroke-width:2px,stroke:#00B4D8,fill:#48CAE4;

classDef newSkillGroup stroke-width:4px,stroke:#D6CCC2,fill:#EDEDE9;
classDef newSkill stroke-width:2px,stroke:#D6CCC2,fill:#EDEDE9;
classDef unknownSkill stroke-width:2px,stroke:#D6CCC2,fill:#EDEDE9;

class url_shortener normalSkillGroup;
```

```mermaid
flowchart TD
url_shortener(fa:fa-hashtag <br/>url shortener)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.webui[fa:fa-desktop web ui]
groups.webui.skills.url_validator(fa:fa-globe <br/>url validator)
class groups.webui.skills.url_validator newSkill;
groups.webui.skills.react-->groups.webui.skills.url_validator
groups.webui.skills.react(fa:fa-list <br/>react)
class groups.webui.skills.react beingLearnedSkill;

end
class groups.webui normalSkillGroup;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.native_client[fa:fa-desktop native client]
groups.native_client.skills.react_native(fa:fa-mobile <br/>react native)
class groups.native_client.skills.react_native newSkill;

groups.native_client.skills.other_clients(fa:fa-lock <br/>???)
class groups.native_client.skills.other_clients unknownSkill;

end
class groups.native_client newSkillGroup;
groups.webui-->groups.native_client

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.backend[fa:fa-server backend]
groups.backend.skills.restapi(fa:fa-send <br/>REST API)
class groups.backend.skills.restapi learnedSkill;

groups.backend.skills.database(fa:fa-database <br/>database)
class groups.backend.skills.database learnedSkill;

end
class groups.backend normalSkillGroup;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.partitioned_backend[fa:fa-copy partitioned backend]
groups.partitioned_backend.skills.proxy(fa:fa-anchor <br/>proxy)
class groups.partitioned_backend.skills.proxy beingLearnedSkill;

groups.partitioned_backend.skills.database(fa:fa-database <br/>partitioned database)
class groups.partitioned_backend.skills.database beingLearnedSkill;

end
class groups.partitioned_backend normalSkillGroup;
groups.backend-->groups.partitioned_backend

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subgraph groups.cache[ cache]
groups.cache.skills.memcache(fa:fa-magnet <br/>memcache)
class groups.cache.skills.memcache learnedSkill;

groups.cache.skills.redis(fa:fa-lock <br/>???)
class groups.cache.skills.redis unknownSkill;

end
class groups.cache normalSkillGroup;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
url_shortener-->groups.webui
url_shortener-->groups.backend
url_shortener-->groups.cache
classDef normalSkillGroup stroke-width:4px,stroke:#DCEBCA,fill:#E9F5DB;
classDef beingLearnedSkill stroke-width:2px,stroke:#C2D5AA,fill:#CFE1B9;
classDef learnedSkill stroke-width:2px,stroke:#A6B98B,fill:#B5C99A;

classDef newSkillGroup stroke-width:4px,stroke:#D6CCC2,fill:#EDEDE9;
classDef newSkill stroke-width:2px,stroke:#D6CCC2,fill:#EDEDE9;
classDef unknownSkill stroke-width:2px,stroke:#D6CCC2,fill:#EDEDE9;

%% https://www.w3schools.com/colors/colors_groups.asp
linkStyle default stroke-width:2px,stroke:OliveDrab;
class url_shortener normalSkillGroup;
```

# License
[MIT License](LICENSE)

# More details
* Skillmap toml descriptor format can be found [here](docs/skillmap_descriptor.md)
* hot reloading when authoring a skillmap toml file
    * install several tools to make hot reloading to work
        * [`entr`](https://github.com/eradman/entr), run arbitrary commands when files change
        * [Visual Studio Code](https://code.visualstudio.com) + [Markdown Preview Enhanced Visual Studio Code Extension](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
        * Basically, use `entr` to watch toml file changes, and generate a `md` makrdown file using `skillmap` every time when toml file changes. And use `vscode` + `Markdown Preview Enhanced` extension to open this generated markdown file. Check out `build_sample` and `dev_sample` in [justfile](justfile) to see how to make hot reloading work