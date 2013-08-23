# coding: utf-8

default_template = u'''<html>
  <head>
    <style>
        body {
            font-family: Helvetica, Arial, Sans-serif;
            padding: 0 2em;
        }

        ul {
            list-style: none;
        }

        table {
            border-collapse: collapse;
        }

        th {
            padding: 10px;
        }

        th, td {
            border: 1px solid #CCC;
            text-align: center;
            padding: 1em;
        }

    </style>
  </head>
  <body>
    <h1>Quality Report for {{ project_name }}</h1>

    <h2>Index</h2>

    <ul>
      <li> <a href="#section-video">Video history</a> </li>
      <li> <a href="#section-top10best">Top-10 best files</a> </li>
      <li> <a href="#section-top10worst">Top-10 worst files</a> </li>
      <li> <a href="#section-tags">Tags (versions released)</a> </li>
      <li> <a href="#section-ratioperfile">Ratio per file</a> </li>
    </ul>


    <h2><a name="section-video">Video History</a></h2>

      <div align="center">
        <video controls="controls" width="800" preload="auto">
        <source src="{{ video_filename }}" type="video/ogg" />
        Your browser does not support HTML5 videos.
        </video>
      </div>


    <h2><a name="section-top10best">Top 10 best files</a></h2>

    <table>
      <tr><th>Filename</th><th>Total lines</th><th>Lines with warnings</th><th>% of lines with warnings</th></tr>
      {% for file in best_files %}
      <tr><td>{{ file.filename }}</td><td>{{ file.total_lines}}</td><td>{{ file.lines_with_errors }}</td><td>{{ '%0.2f'|format(file.ratio|float * 100) }}</tr>
      {% endfor %}
    </table>


    <h2><a name="section-top10worst">Top 10 worst files</a></h2>

    <table>
      <tr><th>Filename</th><th>Total lines</th><th>Lines with warnings</th><th>% of lines with warnings</th></tr>
      {% for file in worst_files %}
      <tr><td>{{ file.filename }}</td><td>{{ file.total_lines}}</td><td>{{ file.lines_with_errors }}</td><td>{{ '%0.2f'|format(file.ratio|float * 100) }}</tr>
      {% endfor %}
    </table>


    <h2><a name="section-tags">Git Tags</a></h2>

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
    <h3><a name="tag-{{ tag.name}} ">Tag {{ tag.name }}</a></h3>

    Date released: {{ tag.date }}
    <br />
    <a href="{{ tag.graph_filename }}"><img src="{{ tag.graph_filename }}"
            alt="PEP8 ratio histogram for {{ project_name }} tag {{ tag.name }}"
            width="800" border="0" /></a>

    {% endfor %}


    <h2><a name="section-ratioperfile">Ratio per file</a></h2>

    <table>
      <tr><th>Filename</th><th>Total lines</th><th>Lines with warnings</th><th>% of lines with warnings</th></tr>
      {% for file in ratios|reverse %}
      <tr><td>{{ file.filename }}</td><td>{{ file.total_lines}}</td><td>{{ file.lines_with_errors }}</td><td>{{ '%0.2f'|format(file.ratio|float * 100) }}</tr>
      {% endfor %}
    </table>
  </body>
</html>'''
