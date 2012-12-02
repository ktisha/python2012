%include header_template username=username

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Login</h2>
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
								{{login_error}}            
								  </td>
								</tr>
							  </table>
							  <input type="submit" value="Login">
							  </form>
						<br/>
						Not registered? <a href="/signup"><u>Sign up</u></a><p>
					</td>
				</tr>
			</table>
		</td>
	</tr>


    

%include footer_template