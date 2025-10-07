#include <stdio.h>
int main() {
	int n;
	scanf("%d", &n);
	float matrix[n][n];
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
		       scanf("%f", &matrix[i][j]);
		}
	}
	for (int j = n - 1; j >= 0; j--) {
		for (int i = n - 1; i >= 0; i--) {
			if (matrix[i][j] == 0) {
				for (int k = 0; k < n; k++) {
					float temp;
					temp = matrix[i][k];
					matrix[i][k] = matrix[i - 1][k];
					matrix[i - 1][k] = temp;
				}
				break;
			}	
			if (i < j && matrix[i][j] != 0) {
				float c = matrix[i][j] / matrix[j][j];
				for (int l = 0; l < n; l++) {
					matrix[i][l] = matrix[i][l] - (c)*matrix[j][l];
				}
			}
		}
	}
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
		       printf("%.2f ", matrix[i][j]);
		}
		printf("\n");
	}

	return 0;
}	
