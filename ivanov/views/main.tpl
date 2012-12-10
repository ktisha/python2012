%include header_template username=username

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Challenges</h2>

						%for challenge in challenges_requests_from_friends:
                            <table>
                            <tr height=40px class="cell">
                                <td width=400px>
                                    <span class="cell_header">{{challenge['achievement']['name']}}</span><br/>
                                    <span class="cell_caption">{{challenge['achievement']['description']}}</span>
                                    <span class="cell_caption">(<a href="/friends?friend={{challenge['from']}}">{{challenge['from']}}</a>)</span>
                                </td>
                                <td width=130px align=center>
                                    <a href="/add_challenge_from_friend?challenge={{challenge['achievement']['_id']}}"><div class="green_button">Accept</div></a>
                                </td>
                                <td width=50px align=center><a href="/reject_challenge_request?challenge={{challenge['achievement']['_id']}}"><img src="/static/cancel.png"/></td>
                            </tr>
                            </table>
                        %end

						%for challenge in challenges:
							<table>
							<tr height=40px class="cell">
								<td width=400px>
									<span class="cell_header">{{challenge['name']}}</span><br/>
									<span class="cell_caption">{{challenge['description']}}</span>
								</td>
								<td width=130px align=center> 
									<a href="/achievement_unlocked?achievement={{challenge['_id']}}"><div class="green_button">Completed!</div></a>
								</td>
								<td width=50px align=center><a href="/reject_challenge?challenge={{challenge['_id']}}"><img src="/static/cancel.png"/></td>
							</tr>  
							</table>								
						%end								
						
						<br/>						
						<table><tr>
						<td><a href="/search"><div class="green_button" align=center>Search</div></a></td>
						<td><a href="/new_achievement"><div class="green_button" align=center>Create new</div></a></td>
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

						%for achievement in achievements_requests_from_friends:
                            <table>
                            <tr height=40px class="cell">
                                <td width=400px>
                                    <span class="cell_header">{{achievement['achievement']['name']}}</span><br/>
                                    <span class="cell_caption">{{achievement['achievement']['description']}}</span>
                                    <span class="cell_caption">(<a href="/friends?friend={{achievement['from']}}">{{achievement['from']}}</a>)</span>
                                </td>
                                <td width=130px align=center>
                                    <a href="/unlock_achievement_from_friend?achievement={{achievement['achievement']['_id']}}"><div class="green_button">Unlock!</div></a>
                                </td>
                                <td width=50px align=center><a href="/reject_achievement_request?achievement={{achievement['achievement']['_id']}}"><img src="/static/cancel.png"/></td>
                            </tr>
                            </table>
                        %end

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
						
						%for friend in friends_requests:							
							<table>
							<tr height=40px class="cell">
								<td width=400px>
									<span class="cell_caption"><a href="/friends?friend={{friend}}">{{friend}}</a></span>
								</td>
								<td width=130px align=center> 
									<a href="/accept_friend_request?friend={{friend}}"><div class="green_button">Accept</div></a>
								</td>
								<td width=50px align=center><a href="/reject_friend_request?friend={{friend}}"><img src="/static/cancel.png"/></td>
							</tr>  
							</table>								
						%end								
						
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
						
						<br/>
						<a href="/add_friend"><div class="green_button" align=center>Add friend</div></a>
					</td>
				</tr>
			</table>
		</td>
	</tr>
	
%include footer_template