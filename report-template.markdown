# Quality Report for {{ project_name }}

## Index

<ul>
  <li> <a href="#section-video">Video history</a> </li>
  <li> <a href="#section-top10best">Top-10 best files</a> </li>
  <li> <a href="#section-top10worst">Top-10 worst files</a> </li>
  <li> <a href="#section-tags">Tags (versions released)</a> </li>
  <li> <a href="#section-ratioperfile">Ratio per file</a> </li>
</ul>


## <a name="section-video">Video History</a>

  <div align="center">
    <video controls="controls" width="800" preload="auto">
    <source src="{{ video_filename }}" type="video/ogg" />
    Your browser does not support HTML5 videos.
    </video>
  </div>


## <a name="section-top10best">Top 10 best files</a>

TODO
<ul>
{% for file in best_files %}
  <li> {{ file.filename }}, {{ file.ratio }} </li>
{% endfor %}
</ul>


## <a name="section-top10worst">Top 10 worst files</a>

TODO
<ul>
{% for file in worst_files %}
  <li> {{ file.filename }}, {{ file.ratio }} </li>
{% endfor %}
</ul>


## <a name="section-tags">Git Tags</a>

<table>
  <tr>
    <th> Name </th>
    <th> Date released </th>
  </tr>

{% for tag in tags %}
  <tr>
    <td> <a href="#tag-{{ tag.name }}">{{ tag.name }}</a> </td>
    <td> {{ tag.date }} </td>
  </tr>
{% endfor %}
</table>

{% for tag in tags %}
### <a name="tag-{{ tag.name}} ">Tag {{ tag.name }}</a>

Date released: {{ tag.date }}
<br />
<a href="{{ tag.graph_filename }}"><img src="{{ tag.graph_filename }}"
        alt="PEP8 ratio histogram for {{ project_name }} tag {{ tag.name }}"
        width="800" border="0" /></a>

{% endfor %}


## <a name="section-ratioperfile">Ratio per file</a>
TODO
