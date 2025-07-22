"""Command-line interface for the Simple Chatbot.

This module provides a CLI interface using Click and Rich
for an enhanced user experience with the chatbot.
"""

import logging
import sys

import click
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import clear
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from simple_chatbot.chatbot import SimpleChatbot
from simple_chatbot.config import ChatbotConfig
from simple_chatbot.llm_client import ModelNotFoundError, OllamaConnectionError

# Initialize Rich console
console = Console()

# Initialize command history
command_history = InMemoryHistory()


# Setup key bindings for additional shortcuts
def create_key_bindings() -> KeyBindings:
    """Create custom key bindings for the prompt."""
    kb = KeyBindings()

    @kb.add("c-l")  # Ctrl+L to clear screen
    def clear_screen(event):  # noqa: F841
        """Clear the screen."""
        clear()
        console.print("🧹 Screen cleared!", style="dim")

    return kb


def setup_logging(debug: bool = False) -> None:
    """Setup logging configuration.

    Args:
        debug: Whether to enable debug logging
    """
    if debug:
        level = logging.DEBUG
        format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        level = logging.WARNING
        format_str = "%(levelname)s: %(message)s"

    logging.basicConfig(
        level=level, format=format_str, handlers=[logging.StreamHandler(sys.stderr)]
    )

    # Reduce verbosity of third-party libraries unless in debug mode
    if not debug:
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)


def display_welcome() -> None:
    """Display welcome message and instructions."""
    welcome_text = Text("Simple Chatbot with RAG", style="bold blue")
    welcome_panel = Panel(
        Text.assemble(
            welcome_text,
            "\n\n",
            "A simple chatbot using LangChain, Ollama and RAG\n",
            "Type '/quit', '/exit', or '/bye' to end the conversation\n",
            "Type '/reset' to clear conversation history\n",
            "Type '/stats' to see conversation statistics\n",
            "Type '/history' to see conversation history\n",
            "Type '/knowledge' to see knowledge base info\n",
            "Type '/search <query>' to search the knowledge base\n",
            "Type '/categories' to see available knowledge categories\n",
            "Type '/reload' to reload the knowledge base\n",
            "Type '/help' to see this message again\n\n",
            "💡 Use ↑↓ arrow keys to navigate command history\n",
            "💡 Use Ctrl+L to clear screen\n",
            "💡 RAG will automatically enhance responses with relevant knowledge",
            style="white",
        ),
        title="Welcome",
        border_style="blue",
    )
    console.print(welcome_panel)
    console.print()


def display_stats(chatbot: SimpleChatbot) -> None:
    """Display conversation and RAG statistics.

    Args:
        chatbot: The chatbot instance
    """
    stats = chatbot.get_conversation_stats()

    table = Table(title="Conversation & RAG Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in stats.items():
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)
    console.print()


def display_knowledge_info(chatbot: SimpleChatbot) -> None:
    """Display knowledge base information.

    Args:
        chatbot: The chatbot instance
    """
    kb_stats = chatbot.get_knowledge_stats()

    if not kb_stats.get("enabled", False):
        console.print("🚫 RAG functionality is disabled", style="yellow")
        console.print()
        return

    table = Table(title="Knowledge Base Information")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in kb_stats.items():
        if key == "categories" and isinstance(value, list):
            value = ", ".join(value) if value else "None"
        table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)
    console.print()


def display_search_results(results: list) -> None:
    """Display knowledge search results.

    Args:
        results: List of search results
    """
    if not results:
        console.print("🔍 No results found", style="yellow")
        console.print()
        return

    for i, result in enumerate(results, 1):
        result_panel = Panel(
            Text.assemble(
                f"Relevance: {result.relevance_score:.2f}\n",
                f"Keywords: {', '.join(result.matched_keywords)}\n",
                f"Category: {result.category or 'None'}\n\n",
                result.content,
                style="white",
            ),
            title=f"Result {i}: {result.entry_id}",
            border_style="cyan",
        )
        console.print(result_panel)

    console.print()


def display_categories(categories: list[str]) -> None:
    """Display available knowledge categories.

    Args:
        categories: List of category names
    """
    if not categories:
        console.print("📂 No categories available", style="yellow")
        console.print()
        return

    table = Table(title="Knowledge Categories")
    table.add_column("Category", style="cyan")

    for category in categories:
        table.add_row(category)

    console.print(table)
    console.print()


def display_error(message: str) -> None:
    """Display an error message.

    Args:
        message: The error message to display
    """
    error_panel = Panel(message, title="Error", border_style="red")
    console.print(error_panel)


def display_bot_response(response: str) -> None:
    """Display the bot's response.

    Args:
        response: The bot's response to display
    """
    bot_panel = Panel(response, title="Bot", border_style="green")
    console.print(bot_panel)


@click.command()
@click.option("--model", default="llama2", help="Ollama model to use (default: llama2)")
@click.option(
    "--temperature",
    default=0.7,
    type=float,
    help="Temperature for text generation (0.0 to 1.0, default: 0.7)",
)
@click.option(
    "--max-tokens",
    default=2000,
    type=int,
    help="Maximum number of tokens to generate (default: 2000)",
)
@click.option(
    "--ollama-url",
    default="http://localhost:11434",
    help="Ollama base URL (default: http://localhost:11434)",
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option(
    "--memory-limit",
    default=10,
    type=int,
    help="Maximum number of message pairs to keep in memory (default: 10)",
)
@click.option(
    "--long-responses",
    is_flag=True,
    help="Allow very long responses (sets max-tokens to 4000)",
)
@click.option(
    "--no-rag",
    is_flag=True,
    help="Disable RAG functionality (default: RAG enabled)",
)
@click.option(
    "--knowledge-file",
    default="data/knowledge.json",
    help="Path to knowledge base file (default: data/knowledge.json)",
)
def main(
    model: str,
    temperature: float,
    max_tokens: int,
    ollama_url: str,
    debug: bool,
    memory_limit: int,
    long_responses: bool,
    no_rag: bool,
    knowledge_file: str,
) -> None:
    """Simple Chatbot CLI - A LangChain, Ollama and RAG powered chatbot.

    This chatbot uses local LLMs through Ollama for conversation with optional
    RAG (Retrieval-Augmented Generation) to enhance responses with relevant knowledge.
    Make sure Ollama is running and the specified model is available.
    """
    # Setup logging
    setup_logging(debug)

    # Adjust max_tokens if long_responses is enabled
    if long_responses:
        max_tokens = 4000
        if debug:
            console.print(
                f"🔧 Long responses enabled: max_tokens set to {max_tokens}",
                style="cyan",
            )

    # Create configuration
    config = ChatbotConfig(
        ollama_base_url=ollama_url,
        model_name=model,
        temperature=temperature,
        max_tokens=max_tokens,
        conversation_memory_limit=memory_limit,
        rag_enabled=not no_rag,
        knowledge_file=knowledge_file,
    )

    # Display welcome message
    display_welcome()

    try:
        # Initialize chatbot
        with console.status("[bold green]Initializing chatbot...", spinner="dots"):
            chatbot = SimpleChatbot(config)

        console.print(f"✅ Connected to Ollama with model: [bold]{model}[/bold]")
        console.print()

        # Health check
        if not chatbot.is_healthy():
            display_error(
                f"Warning: Health check failed. The model '{model}' "
                "might not be available.\n"
                "Please ensure Ollama is running and the model is downloaded."
            )
            console.print()

        # Setup key bindings
        kb = create_key_bindings()

        # Main conversation loop
        while True:
            try:
                # Get user input with history support
                try:
                    user_input = prompt(
                        "You: ",
                        history=command_history,
                        key_bindings=kb,
                        complete_style="column",
                    ).strip()
                except (EOFError, KeyboardInterrupt):
                    console.print("\n👋 Goodbye!", style="bold blue")
                    break

                # Handle special commands (must start with /)
                if user_input.lower() in ["/quit", "/exit", "/bye"]:
                    console.print("👋 Goodbye!", style="bold blue")
                    break
                elif user_input.lower() == "/reset":
                    chatbot.reset_conversation()
                    console.print("🔄 Conversation reset!", style="bold yellow")
                    console.print()
                    continue
                elif user_input.lower() == "/stats":
                    display_stats(chatbot)
                    continue
                elif user_input.lower() == "/history":
                    history = chatbot.get_conversation_history()
                    if history.strip():
                        history_panel = Panel(
                            history, title="Conversation History", border_style="cyan"
                        )
                        console.print(history_panel)
                    else:
                        console.print("No conversation history yet.", style="italic")
                    console.print()
                    continue
                elif user_input.lower() == "/knowledge":
                    display_knowledge_info(chatbot)
                    continue
                elif user_input.lower().startswith("/search "):
                    search_query = user_input[8:].strip()  # Remove "/search " prefix
                    if search_query:
                        with console.status("[bold green]Searching knowledge base...", spinner="dots"):
                            results = chatbot.search_knowledge(search_query)
                        display_search_results(results)
                    else:
                        console.print("💡 Usage: /search <query>", style="yellow")
                        console.print()
                    continue
                elif user_input.lower() == "/categories":
                    categories = chatbot.get_knowledge_categories()
                    display_categories(categories)
                    continue
                elif user_input.lower() == "/reload":
                    with console.status("[bold green]Reloading knowledge base...", spinner="dots"):
                        success = chatbot.reload_knowledge()
                    if success:
                        console.print("✅ Knowledge base reloaded successfully!", style="bold green")
                    else:
                        console.print("❌ Failed to reload knowledge base", style="red")
                    console.print()
                    continue
                elif user_input.lower() == "/help":
                    display_welcome()
                    continue

                # Handle empty input
                elif not user_input:
                    continue

                # Help users who forgot the / prefix
                elif user_input.lower() in [
                    "quit",
                    "exit",
                    "bye",
                    "reset",
                    "stats",
                    "history",
                    "knowledge",
                    "categories",
                    "reload",
                    "help",
                ] or user_input.lower().startswith("search "):
                    console.print(
                        f"💡 Did you mean '/{user_input.lower()}'? "
                        "Commands now require a '/' prefix.",
                        style="yellow",
                    )
                    continue

                # Generate and display response
                with console.status("[bold green]Thinking...", spinner="dots"):
                    response = chatbot.chat(user_input)

                display_bot_response(response)
                console.print()

            except Exception as e:
                if debug:
                    display_error(f"Unexpected error: {e}")
                else:
                    console.print(
                        "❌ An error occurred. Use --debug for details.", style="red"
                    )
                console.print()

    except OllamaConnectionError as e:
        display_error(
            f"Failed to connect to Ollama: {e}\n\n"
            f"Please ensure:\n"
            f"1. Ollama is installed and running\n"
            f"2. The service is accessible at {ollama_url}\n"
            f"3. The model '{model}' is available"
        )
        sys.exit(1)
    except ModelNotFoundError as e:
        display_error(f"Model not found: {e}\n\nTry running: ollama pull {model}")
        sys.exit(1)
    except Exception as e:
        display_error(f"Unexpected error during initialization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
