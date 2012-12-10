%include header_template username=username

    <tr>
        <td align=center>
            <table class="block" width=600px>
                <tr>
                    <td>
                        <h2>{{friend}}</h2>

                        %if isFriend:
                            <a href="/delete_friend?friend={{friend}}"><div class="green_button" align=center>Ignore</div></a>
                        %else:
                            <a href="/add_friend_request?friend={{friend}}"><div class="green_button" align=center>Add friend</div></a>
                        %end

                    </td>
                </tr>
            </table>
        </td>
    </tr>

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Challenges</h2>
						
						%for challenge in challenges:
							<table>
							<tr height=40px class="cell">
								<td width=450px>
									<span class="cell_header">{{challenge['name']}}</span><br/>
									<span class="cell_caption">{{challenge['description']}}</span>
								</td>
								<td width=130px align=center> 
									<a href="/achievement_unlocked?achievement={{challenge['_id']}}&friend={{friend}}"><div class="green_button">Completed!</div></a>
								</td>
							</tr>  
							</table>								
						%end								
						
						<br/>						
						<table><tr>
						<td><a href="/search?friend={{friend}}"><div class="green_button" align=center>Search TODO</div></a></td>
						<td><a href="/new_achievement?friend={{friend}}"><div class="green_button" align=center>Create new TODO</div></a></td>
						</td></table>
					</td>
				</tr>
			</table>
		</td>
	</tr>

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Achievements</h2>
						
						%for achievement in achievements:
							<table>
							<tr height=40px class="cell">
								<td width=580px>
									<span class="cell_header">{{achievement['name']}}</span><br/>
									<span class="cell_caption">{{achievement['description']}}</span>
								</td>								
							</tr>  
							</table>								
						%end	
						
					</td>
				</tr>
			</table>
		</td>
	</tr>
	
	<tr>
		<td align=center >				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Friends</h2>

						%for friend in friends:							
							<table>
							<tr height=30px class="cell">
								<td width=530px>
									<span class="cell_caption"><a href="/friends?friend={{friend}}">{{friend}}</a></span>
							</td>
								<td width=50px align=center><a href="/delete_friend?friend={{friend}}"><img src="/static/cancel.png"/></td>
							</tr>  
							</table>								
						%end

					</td>
				</tr>
			</table>
		</td>
	</tr>
	
%include footer_template