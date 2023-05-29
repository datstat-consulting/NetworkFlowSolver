# NetworkFlowSolver
Custom library for solving network flow problems.

# Preliminaries
Define the objective function.
- Squared mean error:
```
objective_function = lambda x: np.sum((x.reshape(matrix.shape) - matrix)**2)
```
- Total cost:
```
objective_function = lambda x: np.sum(x.reshape(cost_matrix.shape) * cost_matrix)
```

Define the constraints.
- Law of Conservation of Flow:
```
constraints = []
for i in range(matrix.shape[0]):
    # row constraint
    constraints.append({'type': 'eq', 'fun': lambda x, i=i: np.sum(x.reshape(matrix.shape)[i, :]) - np.sum(matrix[i, :])})
    # column constraint
    constraints.append({'type': 'eq', 'fun': lambda x, i=i: np.sum(x.reshape(matrix.shape)[:, i]) - np.sum(matrix[:, i])})
```
- Capacity constraint: 
```for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i, j=j: capacity_matrix[i, j] - x.reshape(matrix.shape)[i, j]})
```
- Minimum flow requirements:
```
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i, j=j: x.reshape(matrix.shape)[i, j] - min_flow_matrix[i, j]})

```
- Supply and demand constraints:
```
for i in range(matrix.shape[0]):
    constraints.append({'type': 'eq', 'fun': lambda x, i=i: np.sum(x.reshape(matrix.shape)[i, :]) - supply[i]})
    constraints.append({'type': 'eq', 'fun': lambda x, i=i: np.sum(x.reshape(matrix.shape)[:, i]) - demand[i]})

```
# Examples
## Social Accounting Matrix balancing
Load the SAM from the CSV file.
```
sam_df = pd.read_csv('sam.csv', index_col=0)
matrix = sam_df.values
```

Define the objective and constraints.
```
objective_function = lambda x: np.sum((x.reshape(matrix.shape) - matrix)**2)

constraints = []
for i in range(matrix.shape[0]):
    # row constraint
    constraints.append({'type': 'eq', 'fun': lambda x, i=i: np.sum(x.reshape(matrix.shape)[i, :]) - np.sum(matrix[i, :])})
    # column constraint
    constraints.append({'type': 'eq', 'fun': lambda x, i=i: np.sum(x.reshape(matrix.shape)[:, i]) - np.sum(matrix[:, i])})
```
Create a NetworkFlowSolver instance.
```
optimizer = NetworkFlowSolver(sam, objective_function, constraints)
```
Solve the problem.
```
optimized_matrix = optimizer.solve()
```
Visualize with custom options.
```
node_options = {'node_color': 'grey', 'node_size': 500}
edge_color = 'red'
figsize = (10, 8)  # Width=10 inches, Height=8 inches
optimizer.visualize_initial_network(node_options, edge_color, figsize)
optimizer.visualize_solution(node_options, edge_color, figsize)
```
Save the balanced SAM.
```
# Convert the optimized matrix to a DataFrame
optimized_df = pd.DataFrame(optimized_matrix, index=sam_df.index, columns=sam_df.columns)

# Save the DataFrame as a CSV
optimized_df.to_csv('balanced_sam.csv')
```
## Transport Flow problem
