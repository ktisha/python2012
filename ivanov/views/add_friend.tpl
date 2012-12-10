%include header_template username=username

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Add friend</h2>
						<form method="post">
						  <table>
							<tr>
							  <td class="label">
								Friend's username
							  </td>
							  <td>
								<input type="text" name="username" value="{{username}}">
							  </td>
							  <td class="error">
							{{username_error}}
							  </td>
							</tr>
						  </table>
						  <input type="submit" value="Add friend request">
						</form>
					</td>
				</tr>
			</table>
		</td>
	</tr>

%include footer_template
