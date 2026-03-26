# Makefile for VyFwMatch

.PHONY: help build-deps build-ipaddrcheck build-vyos-utils clean-deps test lint install dev-install

help:
	@echo "VyFwMatch Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  build-deps        - Build all binary dependencies (ipaddrcheck + vyos-utils)"
	@echo "  build-ipaddrcheck - Build ipaddrcheck binary only"
	@echo "  build-vyos-utils  - Build vyos-utils (validate-value) binary only"
	@echo "  clean-deps        - Clean built dependencies"
	@echo "  test              - Run test suite"
	@echo "  lint              - Run pylint code quality checks"
	@echo "  install           - Install package"
	@echo "  dev-install       - Install package in development mode"

# Build all dependencies
build-deps: build-ipaddrcheck build-vyos-utils

# Build ipaddrcheck
build-ipaddrcheck:
	@echo "Building ipaddrcheck..."
	cd ipaddrcheck && \
	autoreconf -i && \
	./configure && \
	$(MAKE)
	@echo "ipaddrcheck built successfully at: ipaddrcheck/src/ipaddrcheck"

# Build vyos-utils (validate-value)
build-vyos-utils:
	@echo "Building vyos-utils..."
	cd vyos-utils && \
	dune build
	@echo "validate-value built successfully at: vyos-utils/_build/default/src/validate_value.exe"

# Clean built dependencies
clean-deps:
	@echo "Cleaning dependencies..."
	cd ipaddrcheck && $(MAKE) clean || true
	cd vyos-utils && dune clean || true
	@echo "Dependencies cleaned"

# Run tests
test:
	pytest tests/ -v

# Run linting
lint:
	pylint vyfwmatch/ --score=y

# Install package
install:
	pip install .

# Install in development mode
dev-install:
	pip install -e .

# Run tests with coverage
test-cov:
	pytest tests/ --cov=vyfwmatch --cov-report=html --cov-report=term

# Quick validation check
check: lint test
	@echo "All checks passed!"
