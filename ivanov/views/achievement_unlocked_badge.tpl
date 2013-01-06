%include header_template username=username

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td align="center">
						<h2>Achievement unlocked!</h2>

						<img align="center" src="/static/yea.png"/>
                        <br/> <br/>
						<table>
                        <tr height=40px class="cell">
                            <td width=580px>
                                <span class="cell_header">{{achievement['name']}}</span><br/>
                                <span class="cell_caption">{{achievement['description']}}</span>
                            </td>
                        </tr>
                        </table>
                        <br/>
                        <br/>
                        Тут будут кнопки соц.сетей.<br/>
                        А ещё тут может быть ваша реклама ;)

					</td>
				</tr>
			</table>
		</td>
	</tr>

%include footer_template