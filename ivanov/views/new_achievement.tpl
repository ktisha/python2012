%include header_template username=username

	<tr>
		<td align=center>				
			<table class="block" width=600px>
				<tr>
					<td>						
						<h2>Create new achievement</h2>
						<form method="post">
						  <table>
							<tr>
							  <td class="label">
								Name
							  </td>
							  <td>
								<input type="text" name="name" value="{{name}}">
							  </td>
							  <td class="error">
							   {{name_error}}
							  </td>
							</tr>
							
							<tr>
							  <td class="label">
								Description
							  </td>
							  <td>
								<input type="text" name="description" value="{{description}}">
							  </td>
							  <td class="error">           
							  </td>
							</tr>		
							<tr>
							  <td class="label">
								Tags (split by comma)
							  </td>
							  <td>
								<input type="tags" name="tags" value="{{tags}}">
							  </td>
							  <td class="error">           
							  </td>
							</tr>
						  </table>
						  <input type="hidden" name="friend" value="{{friend}}">
						  <input type="submit" value="Create">
						</form>
					</td>
				</tr>
			</table>
		</td>
	</tr>

%include footer_template