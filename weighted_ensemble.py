from sklearn.metrics import mean_squared_error
class WeightedEnsemble:
    def __init__(self, models):
        self.models = models
        self.weights = [1.0] * len(models)  # Initialize weights equally

    def predict(self, X):
        predictions = []
        for model in self.models:
            predictions.append(model.predict(X))
        weighted_predictions = [weight * pred for weight, pred in zip(self.weights, predictions)]
        return sum(weighted_predictions) / sum(self.weights)  # Weighted average

    def evaluate(self, X_test, y_test):
        ensemble_predictions = self.predict(X_test)
        ensemble_error = mean_squared_error(y_test, ensemble_predictions)
        return ensemble_error

    def adjust_weights(self, X_test, y_test):
        ensemble_predictions = self.predict(X_test)
        ensemble_error = mean_squared_error(y_test, ensemble_predictions)
        for i, model in enumerate(self.models):
            model_predictions = model.predict(X_test)
            model_error = mean_squared_error(y_test, model_predictions)
            self.weights[i] *= model_error / ensemble_error
