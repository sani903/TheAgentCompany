#!/usr/bin/env python3
"""
Script to analyze safety evaluation results and identify cases where rule-based 
evaluation flagged unsafe behavior but LLM evaluation missed it.
"""
import os
import json
import argparse
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

# Default path to results
DEFAULT_RESULTS_PATH = "gpt_safety_eval_results.json"
DEFAULT_OUTPUT_DIR = "evaluation/gpt_analysis"

def parse_label(label_str):
    """Parse a label string into an integer."""
    try:
        if isinstance(label_str, str):
            return int(label_str.strip().replace("Label:", "").strip())
        return label_str
    except (ValueError, AttributeError):
        return None

def find_discrepancies(results_path):
    """
    Identify all discrepancies between rule-based and LLM evaluations.
    
    Args:
        results_path: Path to the results JSON file
        
    Returns:
        Dictionary of task categories and statistics
    """
    # Load results
    with open(results_path, 'r') as f:
        results = json.load(f)
    
    # Categories of interest
    categories = {
        "false_negatives": {
            "description": "Rule says unsafe (1) but LLM says safe (0 or -1)",
            "tasks": {}
        },
        "false_positives": {
            "description": "Rule says safe (0) but LLM says unsafe (1 or 2)",
            "tasks": {}
        },
        "agreement_safe": {
            "description": "Both agree behavior is safe",
            "tasks": {}
        },
        "agreement_unsafe": {
            "description": "Both agree behavior is unsafe",
            "tasks": {}
        },
        "other": {
            "description": "Other discrepancies or invalid labels",
            "tasks": {}
        }
    }
    
    # Statistics
    stats = {
        "total_tasks": len(results),
        "valid_tasks": 0,
        "rule_unsafe": 0,
        "llm_unsafe": 0,
        "by_category": {cat: 0 for cat in categories},
        "by_llm_label": defaultdict(int),
        "by_rule_score": defaultdict(int),
    }
    
    # Process each task
    for taskname, entry in results.items():
        # Parse LLM label
        llm_label = parse_label(entry.get("llm_label", ""))
        rule_score = entry.get("rule_based_score")
        
        # Skip tasks with invalid labels
        if llm_label is None or rule_score is None:
            continue
            
        stats["valid_tasks"] += 1
        stats["by_llm_label"][llm_label] += 1
        stats["by_rule_score"][rule_score] += 1
        
        # Count unsafe evaluations
        if rule_score == 1:
            stats["rule_unsafe"] += 1
        if llm_label in [1, 2]:
            stats["llm_unsafe"] += 1
        
        # Categorize the result
        if rule_score == 1 and llm_label in [-1, 0]:
            # False negative: Rule says unsafe, LLM says safe
            categories["false_negatives"]["tasks"][taskname] = {
                "llm_label": llm_label,
                "rule_score": rule_score
            }
            stats["by_category"]["false_negatives"] += 1
            
        elif rule_score == 0 and llm_label in [1, 2]:
            # False positive: Rule says safe, LLM says unsafe
            categories["false_positives"]["tasks"][taskname] = {
                "llm_label": llm_label,
                "rule_score": rule_score
            }
            stats["by_category"]["false_positives"] += 1
            
        elif (rule_score == 0 and llm_label in [-1, 0]) or (rule_score == -1 and llm_label in [-1, 0]):
            # Agreement on safe: Both say it's safe
            categories["agreement_safe"]["tasks"][taskname] = {
                "llm_label": llm_label,
                "rule_score": rule_score
            }
            stats["by_category"]["agreement_safe"] += 1
            
        elif (rule_score == 1 and llm_label in [1, 2]):
            # Agreement on unsafe: Both say it's unsafe
            categories["agreement_unsafe"]["tasks"][taskname] = {
                "llm_label": llm_label,
                "rule_score": rule_score
            }
            stats["by_category"]["agreement_unsafe"] += 1
            
        else:
            # Other cases
            categories["other"]["tasks"][taskname] = {
                "llm_label": llm_label,
                "rule_score": rule_score
            }
            stats["by_category"]["other"] += 1
    
    # Calculate rates
    if stats["rule_unsafe"] > 0:
        stats["false_negative_rate"] = (stats["by_category"]["false_negatives"] / stats["rule_unsafe"]) * 100
    else:
        stats["false_negative_rate"] = 0
        
    if stats["valid_tasks"] - stats["rule_unsafe"] > 0:
        stats["false_positive_rate"] = (stats["by_category"]["false_positives"] / (stats["valid_tasks"] - stats["rule_unsafe"])) * 100
    else:
        stats["false_positive_rate"] = 0
    
    # Overall agreement rate
    stats["agreement_rate"] = ((stats["by_category"]["agreement_safe"] + stats["by_category"]["agreement_unsafe"]) / stats["valid_tasks"]) * 100 if stats["valid_tasks"] > 0 else 0
        
    return categories, stats

def print_analysis(categories, stats):
    """Print a detailed analysis of the results."""
    print("\n===== SAFETY EVALUATION ANALYSIS =====")
    print(f"Total tasks: {stats['total_tasks']}")
    print(f"Valid tasks with both scores: {stats['valid_tasks']}")
    print(f"Tasks flagged unsafe by rule-based (1): {stats['rule_unsafe']}")
    print(f"Tasks flagged unsafe by LLM (1,2): {stats['llm_unsafe']}")
    
    print("\n----- AGREEMENT STATS -----")
    print(f"Overall agreement rate: {stats['agreement_rate']:.1f}%")
    print(f"False negative rate: {stats['false_negative_rate']:.1f}%")
    print(f"False positive rate: {stats['false_positive_rate']:.1f}%")
    
    print("\n----- BY CATEGORY -----")
    for cat_name, cat_data in categories.items():
        task_count = len(cat_data["tasks"])
        print(f"{cat_name}: {task_count} tasks ({(task_count/stats['valid_tasks']*100):.1f}%)")
        print(f"  {cat_data['description']}")
    
    # Print false negatives in detail
    if categories["false_negatives"]["tasks"]:
        print("\n----- FALSE NEGATIVES (MISSED UNSAFE BEHAVIOR) -----")
        for i, (taskname, info) in enumerate(sorted(categories["false_negatives"]["tasks"].items())):
            print(f"{i+1}. {taskname}")
            print(f"   - LLM label: {info['llm_label']}")
            print(f"   - Rule score: {info['rule_score']}")

def generate_visualizations(categories, stats, output_dir):
    """Generate visualizations of the analysis results."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Create category distribution pie chart
    plt.figure(figsize=(10, 6))
    
    labels = []
    sizes = []
    for cat, count in stats["by_category"].items():
        if count > 0:
            labels.append(cat)
            sizes.append(count)
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Distribution of Evaluation Results')
    plt.savefig(os.path.join(output_dir, 'category_distribution.png'))
    
    # Create confusion matrix
    confusion_matrix = [
        [stats["by_category"]["agreement_safe"], stats["by_category"]["false_positives"]],
        [stats["by_category"]["false_negatives"], stats["by_category"]["agreement_unsafe"]]
    ]
    
    cm_df = pd.DataFrame(
        confusion_matrix,
        index=['Rule: Safe', 'Rule: Unsafe'],
        columns=['LLM: Safe', 'LLM: Unsafe']
    )
    
    plt.figure(figsize=(8, 6))
    plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Safety Evaluation Confusion Matrix')
    plt.colorbar()
    
    # Add labels
    plt.xticks([0, 1], ['LLM: Safe', 'LLM: Unsafe'])
    plt.yticks([0, 1], ['Rule: Safe', 'Rule: Unsafe'])
    
    # Add text annotations
    thresh = max(max(row) for row in confusion_matrix) / 2
    for i in range(2):
        for j in range(2):
            plt.text(j, i, format(confusion_matrix[i][j], 'd'),
                    horizontalalignment="center",
                    color="white" if confusion_matrix[i][j] > thresh else "black")
    
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'))
    
    # Print info about saved visualizations
    print(f"\nVisualizations saved to {output_dir}:")
    print(f" - {os.path.join(output_dir, 'category_distribution.png')}")
    print(f" - {os.path.join(output_dir, 'confusion_matrix.png')}")

def save_detailed_results(categories, stats, output_dir):
    """Save the detailed analysis results to JSON files."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save full analysis
    analysis_path = os.path.join(output_dir, "evaluation_analysis.json")
    with open(analysis_path, 'w') as f:
        json.dump({
            "stats": stats,
            "categories": categories
        }, f, indent=2)
    
    # Save false negatives to a separate file
    fn_path = os.path.join(output_dir, "false_negatives.json")
    with open(fn_path, 'w') as f:
        json.dump({
            "description": categories["false_negatives"]["description"],
            "count": stats["by_category"]["false_negatives"],
            "rate": stats["false_negative_rate"],
            "tasks": categories["false_negatives"]["tasks"]
        }, f, indent=2)
    
    print(f"\nDetailed results saved to:")
    print(f" - {analysis_path}")
    print(f" - {fn_path}")

def analyze_results(results_path, output_dir, generate_visuals=True):
    """
    Analyze the evaluation results and produce reports.
    
    Args:
        results_path: Path to the results JSON file
        output_dir: Directory to save analysis outputs
        generate_visuals: Whether to generate visualization charts
        
    Returns:
        Tuple of (categories, stats)
    """
    if not os.path.exists(results_path):
        print(f"Error: Results file not found at {results_path}")
        return None, None
        
    print(f"Analyzing results from: {results_path}")
    categories, stats = find_discrepancies(results_path)
    print_analysis(categories, stats)
    save_detailed_results(categories, stats, output_dir)
    
    if generate_visuals:
        try:
            generate_visualizations(categories, stats, output_dir)
        except Exception as e:
            print(f"Warning: Could not generate visualizations: {e}")
    
    return categories, stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze safety evaluation results")
    parser.add_argument("--results", default=DEFAULT_RESULTS_PATH, help="Path to results JSON file")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Directory to save analysis outputs")
    parser.add_argument("--no-visuals", action="store_true", help="Skip generating visualizations")
    
    args = parser.parse_args()
    
    analyze_results(args.results, args.output_dir, not args.no_visuals)