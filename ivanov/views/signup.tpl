%include header_template username=username

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Signup</h2>
						<form method="post">
						  <table>
							<tr>
							  <td class="label">
								Username
							  </td>
							  <td>
								<input type="text" name="username" value="{{username_value}}">
							  </td>
							  <td class="error">
							{{username_error}}            
							  </td>
							</tr>

							<tr>
							  <td class="label">
								Password
							  </td>
							  <td>
								<input type="password" name="password" value="">
							  </td>
							  <td class="error">
							{{password_error}}            
							  </td>
							</tr>
						  </table>

						  <input type="submit" value="Sign up">
						</form>
						<br/>
						Already a user? <a href="/login"><u>Login</u></a><p>
					</td>
				</tr>
			</table>
		</td>
	</tr>

%include footer_template