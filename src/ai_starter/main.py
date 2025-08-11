"""CLI entrypoint for the AI Python Starter Template.

This module provides the command-line interface for the application using argparse.
It initializes settings and logger, wires ExampleService, and provides commands
for ping and get operations.
"""

import argparse
import json
import sys
from typing import Dict, Any

from .config import get_settings
from .logging import setup_logger, get_logger
from .services.example_service import ExampleService


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="AI Python Starter Template CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="{ping,get}"
    )
    
    # Ping command
    ping_parser = subparsers.add_parser(
        "ping",
        help="Test connection to the API"
    )
    
    # Get command with parameters
    get_parser = subparsers.add_parser(
        "get",
        help="Make GET request with optional parameters"
    )
    get_parser.add_argument(
        "--params",
        action="append",
        metavar="KEY=VALUE",
        help="Query parameters as key=value pairs (can be used multiple times)"
    )
    
    return parser


def parse_params(params_list: list[str]) -> Dict[str, Any]:
    """Parse key=value parameter pairs into a dictionary.
    
    Args:
        params_list: List of "key=value" strings
        
    Returns:
        Dictionary of parsed parameters
        
    Raises:
        ValueError: If parameter format is invalid
    """
    parsed_params = {}
    
    if not params_list:
        return parsed_params
        
    for param in params_list:
        if "=" not in param:
            raise ValueError(f"Invalid parameter format: {param}. Expected 'key=value'")
            
        key, value = param.split("=", 1)
        key = key.strip()
        value = value.strip()
        
        if not key:
            raise ValueError(f"Empty key in parameter: {param}")
            
        # Try to convert value to appropriate type
        if value.lower() in ("true", "false"):
            parsed_params[key] = value.lower() == "true"
        elif value.isdigit():
            parsed_params[key] = int(value)
        elif value.replace(".", "").isdigit() and value.count(".") == 1:
            parsed_params[key] = float(value)
        else:
            parsed_params[key] = value
            
    return parsed_params


def handle_ping_command(service: ExampleService, logger) -> int:
    """Handle the ping command.
    
    Args:
        service: ExampleService instance
        logger: Logger instance
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        logger.info("Executing ping command")
        result = service.ping()
        
        # Print the result
        print(json.dumps(result, indent=2))
        
        # Return appropriate exit code
        return 0 if result.get("success", False) else 1
        
    except Exception as e:
        logger.error(f"Ping command failed: {e}")
        print(json.dumps({"success": False, "error": str(e)}, indent=2))
        return 1


def handle_get_command(service: ExampleService, params: Dict[str, Any], logger) -> int:
    """Handle the get command with parameters.
    
    Args:
        service: ExampleService instance
        params: Query parameters dictionary
        logger: Logger instance
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        logger.info(f"Executing get command with params: {params}")
        result = service.get_with_params(params if params else None)
        
        # Print the result as JSON
        print(json.dumps(result, indent=2))
        return 0
        
    except Exception as e:
        logger.error(f"Get command failed: {e}")
        print(json.dumps({"error": str(e)}, indent=2))
        return 1


def main() -> int:
    """Main entry point for the CLI application.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        # Parse command line arguments
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Initialize settings
        settings = get_settings()
        
        # Setup logger
        setup_logger(settings.log_level)
        logger = get_logger()
        
        logger.info("Starting AI Python Starter Template CLI")
        logger.debug(f"Settings: env={settings.env}, api_base_url={settings.api_base_url}")
        
        # Check if command was provided
        if not args.command:
            parser.print_help()
            return 1
            
        # Initialize the service
        with ExampleService(settings.api_base_url) as service:
            
            if args.command == "ping":
                return handle_ping_command(service, logger)
                
            elif args.command == "get":
                try:
                    params = parse_params(args.params or [])
                    return handle_get_command(service, params, logger)
                except ValueError as e:
                    logger.error(f"Parameter parsing error: {e}")
                    print(f"Error: {e}")
                    return 1
                    
            else:
                logger.error(f"Unknown command: {args.command}")
                parser.print_help()
                return 1
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
