%include header_template username=username

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Search</h2>
						<form method="get">						  
							<input type="text" name="q" value="{{q}}">							  
							<input type="submit" value="Search">
						</form>
					
						<br/>
					
						%if achievements != None and achievements.count()>0:
							%for achievement in achievements:					
								<table>
									<tr height=40px class="cell">
										<td width=450px>
											<span class="cell_header">{{achievement['name']}}</span><br/>
											<span class="cell_caption">{{achievement['description']}}</span>											
										</td>								
										<td width=130px align=center> 
											<a href="/accept_challenge?challenge={{achievement['_id']}}"><div class="green_button">Accept!</div></a>
										</td>											
									</tr>  
								</table>
							%end
						%else:
							No results :(
						%end
										
					</td>
				</tr>
			</table>
		</td>
	</tr>

%include footer_template