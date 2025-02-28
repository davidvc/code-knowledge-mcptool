To create an MCP server using the Python MCP SDK and build it for use with Cline, follow these steps:

1. Install the MCP SDK:
   Use UV (recommended) or pip to install the MCP package:
   ```bash
   uv add "mcp[cli]"
   ```
   or
   ```bash
   pip install mcp
   ```

2. Create a new MCP server project:
   Run the following command to set up a new project:
   ```bash
   uvx create-mcp-server
   ```
   or
   ```bash
   pip install create-mcp-server
   create-mcp-server
   ```
   This will guide you through creating a new MCP server project[3].

3. Implement your server:
   Open the `src/my_server/server.py` file and define your MCP server using the FastMCP class:

   ```python
   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("My Server")

   @mcp.tool()
   def example_tool(param: str) -> str:
       return f"You provided: {param}"

   @mcp.resource("example://{name}")
   def example_resource(name: str) -> str:
       return f"Hello, {name}!"
   ```

4. Build the server:
   Navigate to your project directory and run:
   ```bash
   uv sync --dev --all-extras
   ```

5. Test your server:
   Run the server locally using:
   ```bash
   uv run my-server
   ```

6. Integrate with Cline:
   - Open Cline and navigate to the MCP Server tab.
   - Click "Edit MCP Settings" to open the `cline_mcp_settings.json` file.
   - Add your server configuration:
     ```json
     "mcpServers": {
       "my-server": {
         "command": "python",
         "args": ["-m", "my_server"]
       }
     }
     ```
   - Save the file. Cline will automatically detect the change and start your MCP server[1][4].

7. Test in Cline:
   Use Cline's MCP Inspector to verify the server connection and test its functionality[4].

Remember to thoroughly test your server and keep it updated for optimal performance and security[4].

Citations:
[1] https://github.com/modelcontextprotocol/python-sdk
[2] https://docs.cline.bot/mcp-servers/mcp-server-from-scratch
[3] https://github.com/modelcontextprotocol/create-python-server
[4] https://docs.cline.bot/mcp-servers/mcp-server-from-github
[5] https://modelcontextprotocol.io/quickstart/client
[6] https://www.youtube.com/watch?v=b5pqTNiuuJg
[7] https://www.devshorts.in/p/how-to-build-your-own-mcp-server?action=share
[8] https://github.com/bradfair/mcp-cline-personas