# Links Analysis Project Diagrams

## Project Structure

```mermaid
graph TD
    root["/"] --> src["src/"]
    root --> data["data/"]
    root --> output["output/"]
    root --> others["Other Files"]
    
    src --> utils["utils/"]
    src --> data_proc["data/"]
    src --> scrapers["scrapers/"]
    src --> analysis["analysis/"]
    src --> main["main.py"]
    
    data --> raw["raw/"]
    data --> processed["processed/"]
    
    output --> files["Platform Files"]
```

## Pipeline Overview

```mermaid
graph TD
    A[1. Organize Links] --> B[2. Scrape Websites]
    B --> C[3. Extract Concepts]
    C --> D[4. Generate Platform]
    D --> E[5. Render Documents]
    E --> F[6. Generate Images]
```

## Data Flow Diagram

```mermaid
graph LR
    A[Input Files] --> B[Process]
    B --> C[Output Files]
    
    subgraph process
    B1[Organize] --> B2[Scrape]
    B2 --> B3[Extract]
    B3 --> B4[Analyze]
    B4 --> B5[Render]
    B5 --> B6[Generate Images]
    end
```

## Detailed Process Flow

### 1. Organize Links and Tags

```mermaid
graph TD
    A[Input Files] --> B[Process URLs & Tags]
    B --> C[Save organized_links.json]
```

### 2. Website Scraping

```mermaid
graph TD
    A[Load Links] --> B[Scrape Content]
    B --> C[Save Data]
```

### 3. Concept Extraction

```mermaid
graph TD
    A[Load Content] --> B[Process with LLM]
    B --> C[Save Extracted Concepts]
```

### 4. Political Platform Generation

```mermaid
graph TD
    A[Load Concepts] --> B[Generate Platform]
    B --> C[Save Platform JSON]
```

### 5. Markdown and HTML Rendering

```mermaid
graph TD
    A[Load Platform] --> B[Generate Documents]
    B --> C[Save MD & HTML]
```

### 6. Image Generation

```mermaid
graph TD
    A[Load Platform] --> B[Generate Images]
    B --> C[Save Images]
```

## Command Line Options

```mermaid
graph TD
    A[Parse Arguments] --> B{Run Only Specific Stage?}
    B -->|Yes| C[Run Selected Stage]
    B -->|No| D[Run Full Pipeline]
    
    D --> E{Skip Any Stages?}
    E -->|Yes| F[Skip Selected Stages]
    E -->|No| G[Run All Stages]
```
