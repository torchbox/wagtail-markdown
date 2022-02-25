# ----------------------------------------------------------------------------
# Self-Documented Makefile
# ref: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# ----------------------------------------------------------------------------
.PHONY: help
.DEFAULT_GOAL := help

help:											## ⁉️  - Display help comments for each make command
	@grep -E '^[0-9a-zA-Z_-]+:.*? .*$$'  \
		$(MAKEFILE_LIST)  \
		| awk 'BEGIN { FS=":.*?## " }; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'  \
		| sort

clean:	## 🗑️  - Removes pycache and test media
	@echo "🗑️ - Removing __pycache__ and artifacts"
	find . -name ".tox" -prune -o -type d -name  "__pycache__" -exec rm -r {} +
	if test -d dist; then rm -r dist; fi
	if test -d src/wagtail_markdown.egg-info; then rm -r src/wagtail_markdown.egg-info; fi

package-setup:
	@echo "📦 - Packaging for PyPI"
	python3 setup.py clean --all sdist bdist_wheel

package: clean package-setup  ## 📦 - Package for PyPI

test:  ## 🧪 - Run test suite
	@echo "🧪 - Running test suite"
	tox
