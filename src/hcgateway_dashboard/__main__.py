"""Application entry point for HCGateway Dashboard."""

from hcgateway_dashboard import Dashboard


def main() -> None:
    """Entry point for the Streamlit application."""
    dashboard = Dashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
