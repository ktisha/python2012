<!DOCTYPE HTML>
<html>
 <head>
  <meta charset="utf-8">
  <title>Achievements</title>
  <link rel="stylesheet" type="text/css" href="/static/style.css">
 </head>
 <body>

	<table width=800px align=center>
		<tr>
			<td>
				<!--Header-->
				<table width=800px height=30px class="cell">
					<tr>
						<td align=left class="cell_header"><a href="/main">Achievements</a></td>  
						%if len(username)>0:
							<td align=right class="cell_caption">Welcome, {{username}}! | <a href="/logout">Log out</a></td>
						%end
					</tr>
				</table>
			</td>
		</tr>	