# What2Watch

## Table of Contents

-   [About](#about)
-   [Getting Started](#getting_started)
-   [Usage](#usage)
-   [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

A CLI to pick a random title from a IMDb watchlist or chart.

#### Future Implementation Idea:

Add choose random episode from tv-show functionality, w/ season filtering.

## Getting Started <a name = "getting_started"></a>

### Prerequisites

```
Python 3.10
```

### Installing

Clone repo & CD into it

```
git clone https://github.com/hoxas/what2watch ./what2watch/
cd what2watch
```

Create venv

```
python3 -m venv ./venv/
```

Activate venv

```
source ./venv/bin/activate
```

Install requirements

```
pip install requirements.txt
```

Test (running what2watch folder/module)

```
python .
```

## Usage <a name = "usage"></a>

```
what2watch [options] [URL]
```

### Options:

<table>
<tr><td>Option</td><td>Function</td></tr>
<tr><td>-h --help</td> <td>Show this screen.</td></tr>
<tr><td>--version</td> <td>Show version.</td></tr>
<tr><td>-v --verbose</td> <td>Verbose output.</td></tr>
<tr><td>-q --quiet</td> <td>Quiet output.</td><tr>
<tr><td>-c --config</td> <td>Show config file.</td><tr>
<tr><td>--imdb-path=PATH</td> <td>Set default imdb path in config.<td><tr>
</table>

### Arguments

<table>
<tr><td>Argument</td><td>Accepts</td></tr>
<tr><td>URL</td><td>IMDB Watchlist, chart URL or <a href="#chart_options">chart option</a>.</td></tr>
</table>

### Chart Options <a name = "chart_options"></a>:

<table>
<tr><td>Chart Option</td><td>Chart</td><td>Resolves To</td></tr>
<tr><td>top</td><td>Top 250 Movies Chart (default)</td><td>https://www.imdb.com/chart/top/</td></tr>
<tr><td>bottom</td> <td>Bottom 100 Movies Chart</td><td>https://www.imdb.com/chart/bottom/</td></tr>
<tr><td>box_office</td> <td>Top Box Office Movies Chart</td><td>https://www.imdb.com/chart/boxoffice/</td></tr>
<tr><td>popular</td> <td>Most Popular Movies Chart</td><td>https://www.imdb.com/chart/moviemeter/</td><tr>
</table>

### Examples:

```
what2watch --version
what2watch -h
```

Default imdb path found in the config file:

```
what2watch
```

Custom imdb path (supports public watchlist, chart or chart option)]

```
what2watch https://www.imdb.com/path/to/public/watchlist/
```

Setting default imdb path:

```
what2watch --imdb-path https://www.imdb.com/path/to/public/watchlist/
```
