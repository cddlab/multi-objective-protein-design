OUTPUT_DIR="output"
RESULT_CSV="output/results.csv"
YAML_CONFIG="config.yaml"
uv run main.py\
    "$OUTPUT_DIR" \
    "$RESULT_CSV" \
    "$YAML_CONFIG"