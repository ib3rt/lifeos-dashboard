#!/usr/bin/env python3
"""
SEO Optimizer
Optimizes content for search engines.
"""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SEOConfig:
    target_keyword: str
    title_max_length: int = 60
    description_max_length: int = 160
    min_word_count: int = 300
    heading_count: int = 3


class SEOAnalyzer:
    """Analyze and optimize content for SEO."""
    
    def __init__(self, config: SEOConfig):
        self.config = config
        self.issues = []
        self.score = 100
    
    def analyze_title(self, title: str) -> dict:
        """Analyze title for SEO."""
        result = {
            "title": title,
            "length": len(title),
            "has_keyword": self.config.target_keyword.lower() in title.lower(),
            "score": 100
        }
        
        if len(title) > self.config.title_max_length:
            result["warning"] = "Title too long"
            result["score"] -= 10
        
        if not result["has_keyword"]:
            result["warning"] = "Missing target keyword"
            result["score"] -= 20
        
        self.score = min(self.score, result["score"])
        return result
    
    def analyze_content(self, content: str) -> dict:
        """Analyze content for SEO."""
        word_count = len(content.split())
        
        result = {
            "word_count": word_count,
            "keyword_density": content.lower().count(self.config.target_keyword.lower()) / max(1, word_count) * 100,
            "has_headings": bool(re.search(r'^#{1,6}\s', content, re.MULTILINE)),
            "has_meta_description": False,
            "score": 100
        }
        
        if word_count < self.config.min_word_count:
            result["warning"] = f"Content too short ({word_count} words)"
            result["score"] -= 15
        
        if result["keyword_density"] < 0.5:
            result["warning"] = "Low keyword density"
            result["score"] -= 10
        elif result["keyword_density"] > 3.0:
            result["warning"] = "Keyword stuffing"
            result["score"] -= 15
        
        if not result["has_headings"]:
            result["warning"] = "No headings found"
            result["score"] -= 10
        
        self.score = min(self.score, result["score"])
        return result
    
    def get_optimization_suggestions(self) -> List[str]:
        """Generate optimization suggestions."""
        suggestions = []
        
        if self.score < 80:
            suggestions.append("Consider adding the target keyword to the title")
            suggestions.append("Increase content length to improve depth")
            suggestions.append("Add more headings to improve structure")
        
        return suggestions
    
    def get_final_score(self) -> int:
        """Get final SEO score."""
        return max(0, self.score)


def optimize_title(title: str, keyword: str) -> str:
    """Optimize title for SEO."""
    if keyword.lower() not in title.lower():
        title = f"{title}: {keyword}"
    
    if len(title) > 60:
        title = title[:57] + "..."
    
    return title


def optimize_description(content: str, keyword: str, max_length: int = 160) -> str:
    """Generate meta description from content."""
    # Extract first sentence with keyword
    sentences = content.split('.')
    
    for sentence in sentences:
        if keyword.lower() in sentence.lower():
            desc = sentence.strip() + "."
            return desc[:max_length]
    
    return content[:max_length].split('.')[0] + "."


def main():
    # Example usage
    config = SEOConfig(target_keyword="productivity")
    analyzer = SEOAnalyzer(config)
    
    # Sample analysis
    title_result = analyzer.analyze_title("10 Productivity Tips That Actually Work")
    content_result = analyzer.analyze_content(
        "Productivity is key to success. This article covers productivity tips..."
    )
    
    print("SEO Analysis Results:")
    print(f"Title Score: {title_result['score']}")
    print(f"Content Score: {content_result['score']}")
    print(f"Overall Score: {analyzer.get_final_score()}")
    print(f"Suggestions: {analyzer.get_optimization_suggestions()}")


if __name__ == "__main__":
    main()
