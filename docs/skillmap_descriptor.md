# Skillmap descriptor format
* The skillmap descriptor format is a toml file. Here is a minimal example, see [`examples/hello_world.toml`](examples/hello_world.toml)
* It describes three concepts in the file:
  * `skillmap`: the root key of the toml file. Typically, it is used to represent a project.
  * `group`: a group of skills. In each file, it can have multiple groups in it. You can use `group` to represent sub project/component in a project.
  * `skill`: a specific skill. Each group can have multiple skills in it. You can use `skill` to represent a specific component/module in a sub project/component.
### skillmap toml table
* The `skillmap` toml table can have some fields:
  * `name`: [optional] the name of the skillmap. It will be used as a label in the diagram for the top level node.
  * `icon`: [optional] a fontawsome icon name. It will be used as an icon in the diagram. You can find the fontawsome icon list [here](https://fontawesome.com/v4.7.0/icons/).
  * `theme`: [optional] theme for the diagram. Serveral themes are included:
    * ocean (default theme)
    * earth
    * grape
    * grass
    * pale
    * rose
  * `orientation`: [optional] the orientation of the diagram. [All mermaid's orientations](https://mermaid-js.github.io/mermaid/#/flowchart?id=flowchart-orientation) are supported, including:
    * TB - top to bottom (default)
    * TD - top-down/ same as top to bottom
    * BT - bottom to top
    * RL - right to left
    * LR - left to right
  * `progress_bar_style`: [optional] an integer value as different styles of progress bar. When a skill is specified with a progress (e.g. "1/3"), this property can be used to tell skillmap to render the skill progress bar in different styles. There are currently 28 different styles you can choose from. Simply specify a value between `0` ~ `27` to give it a try. For example, here are two styles `💚🤍🤍`/`■□□` you can choose from.
## group/skill toml tables
* The `group`/`skill` toml table can have some fields:
  * `name`: [optional] the name of the skillmap/group/skill. It will be used as a label in the diagram. .
  * `icon`: [optional] a fontawsome icon name. It will be used as an icon in the diagram. You can find the fontawsome icon list [here](https://fontawesome.com/v4.7.0/icons/).
  * `requires`: [optional] a list of strings. It indicates a list of skill groups or skills to be learned before this learning this skill group/skill. where each string is a toml table name of a group/skill. It will be rendered as an edge(s) from one node to another. 
  * `progress`: [optional] only applies to a `skill` toml table. It is a fraction number string like `1/3` that indicates the learning progression of the skill. A progress bar like `■□□` will be shown in the skill node to visualize the progress. Skill nodes will be rendered with different colors according to different progresses (zero progress, ongoing, finished).
  * `status`: [optional] a string value indicating the status of the skill. Three valid values are supported [new|beingLearned|learned]. When specifying a different status, different colors will be used when rendering the node. Usually, you simply use `progress` to indicate the status. If you do NOT want a progress bar but just want some simple status, you can specify this property.
  * locked skill: if a skill table doesn't have name or icon, it will be rendered as a locked skill (a grey box + lock icon + `???` as name).

## Example
```toml
[groups.learn_python]
name = "learn python"
icon = "rocket"
    [groups.learn_python.skills.string_literal_usage]
    name = "string literal"
    icon = "book"
    progress = "1/3"
    [groups.learn_python.skills.print]
    name = "print statement"
    icon = "printer"
    requires = ["groups.learn_python.skills.string_literal_usage"]

[groups.program_with_python]
name = "program with python"
icon = "car"
requires = ["groups.learn_python"]
```
In this exmaple, there are:
* two groups: `groups.learn_python` and `groups.program_with_python`
* `groups.learn_python` has two skills: 
  * `groups.learn_python.skills.string_literal_usage`
    * this skill's learning progress is `1/3`
  * `groups.learn_python.skills.print` 
    * this skill requires `groups.learn_python.skills.string_literal_usage` to be learned first
* `groups.program_with_python` requires `groups.learn_python` to be learned first. When drawn in the diagram, it will be rendered as an edge from `groups.learn_python` to `groups.program_with_python`.