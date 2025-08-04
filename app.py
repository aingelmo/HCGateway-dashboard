"""Modern entry point for HCGateway Dashboard using the new package structure."""

from hcgateway_dashboard import Dashboard


def main() -> None:
    """Run the HCGateway Dashboard application."""
    dashboard = Dashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
