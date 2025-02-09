import requests
import os
from dotenv import load_dotenv
from typing import List, Dict

class RecommendationService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('HF_API_KEY')
        # Using a text classification model via API
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        print("RecommendationService initialized with API configuration")

    def get_course_recommendations(self, user_profile: Dict, available_courses: List[Dict]) -> List[Dict]:
        """
        Generate personalized course recommendations based on user profile and goals
        """
        user_interests = " ".join(user_profile.get('preferences', {}).get('interests', []))
        user_goals = " ".join(user_profile.get('goals', []))
        
        recommendations = []
        for course in available_courses:
            # Calculate relevance score using the API
            score = self._calculate_relevance(
                user_interests + " " + user_goals,
                course['description']
            )
            recommendations.append({
                'course': course,
                'score': score
            })
        
        # Sort by relevance score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return [r['course'] for r in recommendations[:5]]

    def _calculate_relevance(self, user_profile: str, course_description: str) -> float:
        """
        Calculate relevance score between user profile and course using API
        """
        try:
            payload = {
                "inputs": [course_description, user_profile],
                "parameters": {
                    "candidate_labels": ["relevant", "not relevant"]
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Get score for "relevant" label
                scores = result.get('scores', [0, 0])
                return scores[0] if result.get('labels', ['', ''])[0] == 'relevant' else 0
            else:
                print(f"API Error {response.status_code}: {response.text}")
                return 0
                
        except Exception as e:
            print(f"Error calculating relevance: {str(e)}")
            return 0

    def update_recommendations(self, user_feedback: Dict, current_recommendations: List[Dict]) -> List[Dict]:
        """
        Update recommendations based on user feedback
        """
        # Simple reranking based on feedback
        if user_feedback.get('liked'):
            # Move similar courses up
            return self._rerank_recommendations(current_recommendations, user_feedback)
        return current_recommendations

    def _rerank_recommendations(self, recommendations: List[Dict], feedback: Dict) -> List[Dict]:
        """
        Rerank recommendations based on feedback
        """
        # Simple implementation - could be enhanced with more sophisticated logic
        liked_course = feedback.get('course_id')
        if not liked_course or not recommendations:
            return recommendations
            
        # Move similar courses up
        reranked = []
        others = []
        
        for rec in recommendations:
            if self._is_similar(rec, liked_course):
                reranked.append(rec)
            else:
                others.append(rec)
                
        return reranked + others

    def _is_similar(self, course: Dict, liked_course_id: str) -> bool:
        """
        Check if a course is similar to the liked course
        """
        # Simple implementation - could be enhanced
        return any(topic in course.get('topics', []) 
                  for topic in self._get_course_topics(liked_course_id))

    def _get_course_topics(self, course_id: str) -> List[str]:
        """
        Get topics for a course
        """
        # This would typically fetch from database
        # Simplified implementation
        return ['programming', 'web development', 'python'] 