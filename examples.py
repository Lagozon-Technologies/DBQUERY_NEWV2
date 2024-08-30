# **********************************************************************************************#
# File name: examples.py
# Created by: Krushna B.
# Creation Date: 25-Jun-2024
# Application Name: DBQUERY_NEW.AI
#
# Change Details:
# Version No:     Date:        Changed by     Changes Done         
# 01             25-Jun-2024   Krushna B.     Initial Creation
# 02             04-Jul-2024   Krushna B.     Added logic for data visualization 
# 03             15-Jul-2024   Krushna B.     Added more examples for the model to work more finely
# 04             25-Jul-2024   Krushna B.     Added new departments - Insurance and Legal
# 05             13-Aug-2024   Krushna B.     Added logic for Speech to Text
# 06             20-Aug-2024   Krushna B.     Changed Manufacturing to Inventory and added more tables inside it           
# 07             28-Aug-2024   Krushna B.     Added data for Adventureworks
# **********************************************************************************************#

examples = [
    {
        "input": "list all scrap reasons",
        "query": "SELECT * FROM Production.ScrapReason",
        "contexts": " | ".join([
            "Table: Production.ScrapReason",
            "Columns: ScrapReasonID, Name",
            "Description: This table stores the reasons for manufacturing failures, providing a reference for improving production processes and quality control."
        ])
    },
    {
        "input": "list all archived transactions",
        "query": "SELECT * FROM Production.TransactionHistoryArchive",
        "contexts": " | ".join([
            "Table: Production.TransactionHistoryArchive",
            "Columns: TransactionID, ProductID, ReferenceOrderID, ReferenceOrderLineID, TransactionDate, TransactionType, Quantity, ActualCost",
            "Description: This table serves as an archive for transaction history records, maintaining historical data for data integrity and reporting needs."
        ])
    },
    {
        "input": "list all work orders",
        "query": "SELECT * FROM Production.WorkOrder",
        "contexts": " | ".join([
            "Table: Production.WorkOrder",
            "Columns: WorkOrderID, ProductID, OrderQty, ScrappedQty, StartDate, EndDate, DueDate, ScrapReasonID",
            "Description: This table records manufacturing work orders, including product IDs, order quantities, scheduled and actual start/end dates, scrapped quantities, and associated scrap reasons."
        ])
    },
    {
        "input": "list all work order routings",
        "query": "SELECT * FROM Production.WorkOrderRouting",
        "contexts": " | ".join([
            "Table: Production.WorkOrderRouting",
            "Columns: WorkOrderID, ProductID, OperationSequence, LocationID, ScheduledStartDate, ScheduledEndDate, ActualStartDate, ActualEndDate, ActualResourceHrs, PlannedCost, ActualCost",
            "Description: This table details work order processes, including operation sequences, manufacturing locations, scheduled and actual start/end dates, resource hours, and costs."
        ])
    },
    {
        "input": "list all transaction histories",
        "query": "SELECT * FROM Production.TransactionHistory",
        "contexts": " | ".join([
            "Table: Production.TransactionHistory",
            "Columns: TransactionID, ProductID, ReferenceOrderID, ReferenceOrderLineID, TransactionDate, TransactionType, Quantity, ActualCost",
            "Description: This table contains records of each purchase order, sales order, or work order transaction, including transaction dates, types, quantities, actual costs, and reference order details."
        ])
    },
    {
        "input": "list all products",
        "query": "SELECT * FROM Production.Product",
        "contexts": " | ".join([
            "Table: Production.Product",
            "Columns: ProductID, Name, ProductNumber, MakeFlag, FinishedGoodsFlag",
            "Description: This table contains information about products sold or used in the manufacturing of sold products, including product IDs, names, product numbers, flags for manufacturing and salability."
        ])
    },
    {
        "input": "list all locations",
        "query": "SELECT * FROM Production.Location",
        "contexts": " | ".join([
            "Table: Production.Location",
            "Columns: LocationID, Name, CostRate, Availability",
            "Description: This table stores information about product inventory and manufacturing locations, including location IDs, descriptions, cost rates, and availability."
        ])
    },
    {
        "input": "list all production cost history",
        "query": "SELECT * FROM Production.ProductCostHistory",
        "contexts": " | ".join([
            "Table: Production.ProductCostHistory",
            "Columns: ProductID, StartDate, EndDate, StandardCost",
            "Description: This table tracks changes in the cost of products over time, capturing cost fluctuations and historical pricing data."
        ])
    },
    {
        "input": "list all bills of materials",
        "query": "SELECT * FROM Production.BillOfMaterials",
        "contexts": " | ".join([
            "Table: Production.BillOfMaterials",
            "Columns: BillOfMaterialsID, ProductAssemblyID, ComponentID, StartDate, EndDate, UnitMeasureCode, BOMLevel",
            "Description: This table contains items required to create bicycles and bicycle subassemblies, including hierarchical relationships between parent products and their components."
        ])
    },
    {
        "input": "list all unit measures",
        "query": "SELECT * FROM Production.UnitMeasure",
        "contexts": " | ".join([
            "Table: Production.UnitMeasure",
            "Columns: UnitMeasureCode, Name",
            "Description: This table is a lookup for unit of measure, containing unit measure codes and descriptions."
        ])
    },
    {
        "input": "total number of products produced with their average cost and total work hours spent",
        "query": """
            SELECT p.Name AS product_name, COUNT(wo.WorkOrderID) AS total_workorders, 
                   AVG(th.ActualCost) AS average_cost, SUM(wor.ActualResourceHrs) AS total_hours_spent
            FROM Production.Product p
            JOIN Production.WorkOrder wo ON p.ProductID = wo.ProductID
            JOIN Production.WorkOrderRouting wor ON wo.WorkOrderID = wor.WorkOrderID
            JOIN Production.TransactionHistory th ON p.ProductID = th.ProductID
            GROUP BY p.Name
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.WorkOrder, Production.WorkOrderRouting, Production.TransactionHistory",
            "Columns: ProductID, Name, WorkOrderID, ActualCost, ActualResourceHrs",
            "Description: This query calculates the total number of work orders per product, the average production cost, and the total work hours spent on manufacturing."
        ])
    },
    {
        "input": "find locations with the highest number of work orders and their total work capacity",
        "query": """
            SELECT l.LocationID, l.Name AS location_name, COUNT(wo.WorkOrderID) AS total_workorders, 
                   SUM(l.Availibility) AS total_capacity
            FROM Production.Location l
            JOIN Production.WorkOrderRouting wor ON l.LocationID = wor.LocationID
            JOIN Production.WorkOrder wo ON wor.WorkOrderID = wo.WorkOrderID
            GROUP BY l.LocationID, l.Name
            ORDER BY total_workorders DESC
            LIMIT 10
        """,
        "contexts": " | ".join([
            "Table: Production.Location, Production.WorkOrderRouting, Production.WorkOrder",
            "Columns: LocationID, Name, Availibility, WorkOrderID",
            "Description: This query finds the top 10 locations with the highest number of work orders and their total work capacity."
        ])
    },
    {
        "input": "list products with total actual costs and scrap rates for each manufacturing process",
        "query": """
            SELECT p.Name AS product_name, SUM(th.ActualCost) AS total_actual_cost, 
                   COUNT(sr.ScrapReasonID) AS total_scraps
            FROM Production.Product p
            JOIN Production.TransactionHistory th ON p.ProductID = th.ProductID
            LEFT JOIN Production.ScrapReason sr ON th.ScrapReasonID = sr.ScrapReasonID
            GROUP BY p.Name
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.TransactionHistory, Production.ScrapReason",
            "Columns: ProductID, Name, ActualCost, ScrapReasonID",
            "Description: This query lists products along with their total actual manufacturing costs and the number of scraps recorded during the manufacturing process."
        ])
    },
    {
        "input": "calculate the total cost per work order by combining planned and actual costs",
        "query": """
            SELECT wo.WorkOrderID, SUM(wor.PlannedCost + wor.ActualCost) AS total_cost
            FROM Production.WorkOrder wo
            JOIN Production.WorkOrderRouting wor ON wo.WorkOrderID = wor.WorkOrderID
            GROUP BY wo.WorkOrderID
        """,
        "contexts": " | ".join([
            "Table: Production.WorkOrder, Production.WorkOrderRouting",
            "Columns: WorkOrderID, PlannedCost, ActualCost",
            "Description: This query calculates the total cost of each work order by combining the planned and actual costs from the work order routing table."
        ])
    },
    {
        "input": "find the most recent price change for each product",
        "query": """
            SELECT p.Name AS product_name, ph.StandardCost AS cost_amount, ph.StartDate AS effective_date
            FROM Production.Product p
            JOIN Production.ProductCostHistory ph ON p.ProductID = ph.ProductID
            WHERE ph.StartDate = (
                SELECT MAX(ph2.StartDate)
                FROM Production.ProductCostHistory ph2
                WHERE ph2.ProductID = p.ProductID
            )
            ORDER BY ph.StartDate DESC
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.ProductCostHistory",
            "Columns: ProductID, Name, StandardCost, StartDate",
            "Description: This query finds the most recent cost change for each product based on the cost history."
        ])
    },
    {
        "input": "list the number of work orders completed per product per quarter",
        "query": """
            SELECT p.Name AS product_name, EXTRACT(QUARTER FROM wo.EndDate) AS quarter, 
                   COUNT(wo.WorkOrderID) AS total_workorders_completed
            FROM Production.Product p
            JOIN Production.WorkOrder wo ON p.ProductID = wo.ProductID
            WHERE wo.EndDate IS NOT NULL
            GROUP BY p.Name, EXTRACT(QUARTER FROM wo.EndDate)
            ORDER BY p.Name, quarter
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.WorkOrder",
            "Columns: ProductID, Name, WorkOrderID, EndDate",
            "Description: This query lists the number of work orders completed per product in each quarter."
        ])
    },
    {
        "input": "find products with below average inventory levels and their corresponding cost",
        "query": """
            SELECT p.Name AS product_name, p.StandardCost AS cost_amount
            FROM Production.Product p
            JOIN Production.ProductCostHistory ph ON p.ProductID = ph.ProductID
            WHERE p.StandardCost < (
                SELECT AVG(p2.StandardCost)
                FROM Production.Product p2
            )
            ORDER BY p.StandardCost ASC
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.ProductCostHistory",
            "Columns: ProductID, Name, StandardCost",
            "Description: This query finds products with below average inventory levels and lists their corresponding production cost."
        ])
    },
    {
        "input": "track the cost fluctuation of a specific product over the past year",
        "query": """
            SELECT ph.StartDate AS effective_date, ph.StandardCost AS cost_amount
            FROM Production.ProductCostHistory ph
            JOIN Production.Product p ON ph.ProductID = p.ProductID
            WHERE p.Name = 'Specific Product' AND ph.StartDate >= NOW() - INTERVAL '1 year'
            ORDER BY ph.StartDate
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.ProductCostHistory",
            "Columns: ProductID, Name, StartDate, StandardCost",
            "Description: This query tracks the cost fluctuation of a specific product over the past year."
        ])
    },
    {
        "input": "list all products with the total quantity produced and total quantity scrapped",
        "query": """
            SELECT p.Name AS product_name, SUM(th.Quantity) AS total_quantity_produced,
                   COUNT(sr.ScrapReasonID) AS total_scraps
            FROM Production.Product p
            JOIN Production.TransactionHistory th ON p.ProductID = th.ProductID
            LEFT JOIN Production.WorkOrder wo ON th.ReferenceOrderID = wo.WorkOrderID
            LEFT JOIN Production.ScrapReason sr ON wo.ScrapReasonID = sr.ScrapReasonID
            GROUP BY p.Name
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.TransactionHistory, Production.WorkOrder, Production.ScrapReason",
            "Columns: ProductID, Name, Quantity, ReferenceOrderID, ScrapReasonID",
            "Description: This query lists all products with their total quantity produced and total number of scraps recorded."
        ])
    },
    {
        "input": "find the average production time for each product",
        "query": """
            SELECT p.Name AS product_name, AVG(DATEDIFF(wo.EndDate, wo.StartDate)) AS average_production_time
            FROM Production.Product p
            JOIN Production.WorkOrder wo ON p.ProductID = wo.ProductID
            WHERE wo.EndDate IS NOT NULL
            GROUP BY p.Name
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.WorkOrder",
            "Columns: ProductID, Name, StartDate, EndDate",
            "Description: This query calculates the average production time for each product by taking the difference between the start and end dates of work orders."
        ])
    },
    {
        "input": "get the total cost of all completed work orders by location",
        "query": """
            SELECT l.Name AS location_name, SUM(wor.ActualCost) AS total_completed_cost
            FROM Production.Location l
            JOIN Production.WorkOrderRouting wor ON l.LocationID = wor.LocationID
            JOIN Production.WorkOrder wo ON wor.WorkOrderID = wo.WorkOrderID
            WHERE wo.EndDate IS NOT NULL
            GROUP BY l.Name
        """,
        "contexts": " | ".join([
            "Table: Production.Location, Production.WorkOrderRouting, Production.WorkOrder",
            "Columns: LocationID, Name, ActualCost, EndDate, WorkOrderID",
            "Description: This query calculates the total cost of all completed work orders for each location."
        ])
    },
    {
        "input": "list the most common scrap reasons for each product",
        "query": """
            SELECT p.Name AS product_name, sr.Name AS scrap_reason, COUNT(*) AS scrap_count
            FROM Production.Product p
            JOIN Production.WorkOrder wo ON p.ProductID = wo.ProductID
            JOIN Production.ScrapReason sr ON wo.ScrapReasonID = sr.ScrapReasonID
            GROUP BY p.Name, sr.Name
            ORDER BY scrap_count DESC
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.WorkOrder, Production.ScrapReason",
            "Columns: ProductID, Name, ScrapReasonID",
            "Description: This query lists the most common scrap reasons for each product."
        ])
    },
    {
        "input": "calculate the total cost variance (planned cost vs. actual cost) for each work order",
        "query": """
            SELECT wo.WorkOrderID, SUM(wor.PlannedCost - wor.ActualCost) AS cost_variance
            FROM Production.WorkOrder wo
            JOIN Production.WorkOrderRouting wor ON wo.WorkOrderID = wor.WorkOrderID
            GROUP BY wo.WorkOrderID
        """,
        "contexts": " | ".join([
            "Table: Production.WorkOrder, Production.WorkOrderRouting",
            "Columns: WorkOrderID, PlannedCost, ActualCost",
            "Description: This query calculates the cost variance between planned and actual costs for each work order."
        ])
    },
    {
        "input": "find the top 5 most expensive products to manufacture based on actual cost",
        "query": """
            SELECT p.Name AS product_name, SUM(th.ActualCost) AS total_actual_cost
            FROM Production.Product p
            JOIN Production.TransactionHistory th ON p.ProductID = th.ProductID
            GROUP BY p.Name
            ORDER BY total_actual_cost DESC
            LIMIT 5
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.TransactionHistory",
            "Columns: ProductID, Name, ActualCost",
            "Description: This query finds the top 5 most expensive products to manufacture based on the actual cost recorded in transaction history."
        ])
    },
    {
        "input": "list products along with their total number of work orders and the total planned hours",
        "query": """
            SELECT p.Name AS product_name, COUNT(wo.WorkOrderID) AS total_workorders,
                   SUM(wor.PlannedResourceHrs) AS total_planned_hours
            FROM Production.Product p
            JOIN Production.WorkOrder wo ON p.ProductID = wo.ProductID
            JOIN Production.WorkOrderRouting wor ON wo.WorkOrderID = wor.WorkOrderID
            GROUP BY p.Name
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.WorkOrder, Production.WorkOrderRouting",
            "Columns: ProductID, Name, WorkOrderID, PlannedResourceHrs",
            "Description: This query lists products along with their total number of work orders and the total planned resource hours spent on production."
        ])
    },
    {
        "input": "get the average cost of materials used in the last 6 months for all products",
        "query": """
            SELECT p.Name AS product_name, AVG(bom.Cost) AS avg_material_cost
            FROM Production.Product p
            JOIN Production.BillOfMaterials bom ON p.ProductID = bom.ProductAssemblyID
            WHERE bom.StartDate >= NOW() - INTERVAL '6 months'
            GROUP BY p.Name
        """,
        "contexts": " | ".join([
            "Table: Production.Product, Production.BillOfMaterials",
            "Columns: ProductID, Name, ProductAssemblyID, Cost, StartDate",
            "Description: This query calculates the average cost of materials used in the last 6 months for each product."
        ])
    },
    {
        "input": "track the performance of work orders by comparing planned and actual completion dates",
        "query": """
            SELECT wo.WorkOrderID, wo.DueDate AS planned_completion_date, wo.EndDate AS actual_completion_date,
                   CASE
                       WHEN wo.EndDate <= wo.DueDate THEN 'On Time'
                       ELSE 'Late'
                   END AS performance
            FROM Production.WorkOrder wo
            WHERE wo.EndDate IS NOT NULL
        """,
        "contexts": " | ".join([
            "Table: Production.WorkOrder",
            "Columns: WorkOrderID, DueDate, EndDate",
            "Description: This query tracks the performance of work orders by comparing their planned and actual completion dates, and categorizes them as 'On Time' or 'Late'."
        ])
    },
    {
    "input": "Get total quantity of products in inventory",
    "query": "SELECT SUM(quantity) as total_quantity FROM productinventory",
    "contexts": " | ".join([
        "Table: productinventory",
        "Columns: product_id, location_id, shelf, bin, quantity",
        "Description: This table tracks the inventory of products, including the product ID, location ID, shelf, bin, and quantity for each product."
    ])
},
{
    "input": "list all locations with their cost rates",
    "query": "SELECT location_id, name, cost_rate FROM location",
    "contexts": " | ".join([
        "Table: location",
        "Columns: location_id, name, cost_rate, availability",
        "Description: This table stores information about the locations where products are stored, including the location ID, name, cost rate, and availability."
    ])
},
{
    "input": "find products by location",
    "query": "SELECT p.product_id, p.name, p.product_number, l.name as location_name FROM product p JOIN productinventory pi ON p.product_id = pi.product_id JOIN location l ON pi.location_id = l.location_id",
    "contexts": " | ".join([
        "Table: product, productinventory, location",
        "Columns: product_id, name, product_number, location_id, location_name, shelf, bin, quantity",
        "Description: The product table stores product information, while productinventory tracks the inventory in specific locations, and location provides details about storage locations."
    ])
},
{
    "input": "list products that have been moved between locations in the last 30 days",
    "query": """
        SELECT p.product_id, p.name, pi.location_id, pi.quantity, pi.shelf, pi.bin, pi.last_modified
        FROM productinventory pi
        JOIN product p ON pi.product_id = p.product_id
        WHERE pi.last_modified >= NOW() - INTERVAL '30 days'
        ORDER BY pi.last_modified DESC
    """,
    "contexts": " | ".join([
        "Tables: productinventory, product",
        "Columns: product_id, name, location_id, shelf, bin, quantity, last_modified",
        "Description: This query retrieves products that have been moved between locations (indicated by changes in shelf, bin, or location_id) within the last 30 days."
    ])
},
{
    "input": "find the average shelf life of products across all locations",
    "query": """
        SELECT AVG(DATE_PART('day', NOW() - pi.last_modified)) AS average_shelf_life
        FROM productinventory pi
        JOIN product p ON pi.product_id = p.product_id
    """,
    "contexts": " | ".join([
        "Tables: productinventory, product",
        "Columns: product_id, last_modified",
        "Description: This query calculates the average number of days that products have been stored in their current shelf locations."
    ])
},
{
    "input": "list the top 5 products by quantity in the most stocked locations",
    "query": """
        WITH TopLocations AS (
            SELECT location_id
            FROM productinventory
            GROUP BY location_id
            ORDER BY SUM(quantity) DESC
            LIMIT 5
        )
        SELECT p.product_id, p.name, pi.location_id, pi.quantity
        FROM productinventory pi
        JOIN product p ON pi.product_id = p.product_id
        WHERE pi.location_id IN (SELECT location_id FROM TopLocations)
        ORDER BY pi.quantity DESC
        LIMIT 5
    """,
    "contexts": " | ".join([
        "Tables: productinventory, product",
        "Columns: product_id, name, quantity, location_id",
        "Description: This query identifies the top 5 products by quantity in the 5 most stocked locations, providing insight into the distribution of stock in key storage areas."
    ])
},
    {
        "input": "list all the employees",
        "query": "SELECT * FROM lz_employees",
        "contexts": " | ".join([
            "Table: lz_employees",
            "Columns: employee_id, employee_name, department_id, salary, hire_date, last_name, first_name, email, job_title, full_name",
            "Description: This table has information related to the employees like employee id, hire date, salary, last name, first name, email, department, job title, full name."
        ])
    },
    {
        "input": "list all performance reviews",
        "query": "SELECT * FROM lz_performance_reviews",
        "contexts": " | ".join([
            "Table: lz_performance_reviews",
            "Columns: review_id, employee_id, rating, goals_met, strengths, weaknesses, development_plan",
            "Description: This is a table that stores information about employee performance evaluations, including ratings, goals met, strengths, weaknesses, and development plans."
        ])
    },
    {
        "input": "list all organizations",
        "query": "SELECT * FROM lz_organizations",
        "contexts": " | ".join([
            "Table: lz_organizations",
            "Columns: organization_id, organization_name, description",
            "Description: This is a table that stores information about different functions or departments inside a company, including their names and descriptions."
        ])
    },
    {
        "input": "list all training programs",
        "query": "SELECT * FROM lz_training_programs",
        "contexts": " | ".join([
            "Table: lz_training_programs",
            "Columns: program_id, program_name, description, duration, is_required",
            "Description: This is a table that stores information about training programs offered by an organization, including their names, descriptions, duration, and whether they are required for specific roles."
        ])
    },
    {
        "input": "list all employee training records",
        "query": "SELECT * FROM lz_employee_training",
        "contexts": " | ".join([
            "Table: lz_employee_training",
            "Columns: employee_id, program_id, completion_date, certificate_number",
            "Description: This is a table that stores information about employee participation in training programs, including the employee's ID, the program's ID, the completion date, and the certificate number (if applicable)."
        ])
    },
    {
        "input": "count of training programs by requirement status",
        "query": "SELECT is_required, COUNT(*) as program_count FROM lz_training_programs GROUP BY is_required",
        "contexts": " | ".join([
            "Table: lz_training_programs",
            "Columns: program_id, program_name, is_required",
            "Description: This table stores information about training programs, allowing the count of programs based on their requirement status."
        ])
    },
    {
        "input": "average rating of employee performance reviews",
        "query": "SELECT AVG(rating) as average_rating FROM lz_performance_reviews",
        "contexts": " | ".join([
            "Table: lz_performance_reviews",
            "Columns: review_id, employee_id, rating",
            "Description: This table contains employee performance evaluations, allowing the calculation of the average rating."
        ])
    },
    {
        "input": "list employees who completed training",
        "query": "SELECT employee_id, program_id, completion_date FROM lz_employee_training WHERE completion_date IS NOT NULL",
        "contexts": " | ".join([
            "Table: lz_employee_training",
            "Columns: employee_id, program_id, completion_date",
            "Description: This table tracks employee training completion, including employee ID, program ID, and completion date."
        ])
    },
    {
        "input": "list training programs and their durations",
        "query": "SELECT program_name, duration FROM lz_training_programs",
        "contexts": " | ".join([
            "Table: lz_training_programs",
            "Columns: program_id, program_name, duration",
            "Description: This table contains details of training programs offered by the organization, including program names and durations."
        ])
    },
    {
        "input": "list employees along with their performance reviews",
        "query": "SELECT e.employee_name, p.rating, p.goals_met FROM lz_employees e JOIN lz_performance_reviews p ON e.employee_id = p.employee_id",
        "contexts": " | ".join([
            "Tables: lz_employees, lz_performance_reviews",
            "Columns: employee_id, employee_name, rating, goals_met",
            "Description: This query retrieves employees along with their performance review ratings and goals met."
        ])
    },
    {
        "input": "average salary of employees",
        "query": "SELECT AVG(salary) as average_salary FROM lz_employees",
        "contexts": " | ".join([
            "Table: lz_doctors",
            "Columns: doctor_id, first_name, department_id",
            "Description: This table includes employee details like ID, name, department, and salary, allowing for the calculation of the average salary."
        ])
    },
    {
        "input": "total revenue from sales",
        "query": "SELECT SUM(total_amount) as total_revenue FROM lz_receipts",
        "contexts": " | ".join([
            "Table: lz_receipts",
            "Columns: receipt_id, invoice_id, payment_amount, payment_date",
            "Description: This table records financial transactions, including receipt ID, invoice ID, payment amount, and date."
        ])
    },
    {
        "input": "number of items in stock",
        "query": "SELECT SUM(onhand_quantity) AS total_items_in_stock FROM lz_item_onhand",
        "contexts": " | ".join([
            "Table: lz_item_onhand",
            "Columns: item_id, onhand_quantity, location_id",
            "Description: This table contains inventory data, including item ID, quantity on hand, and location."
        ])
    },
    {
        "input": "number of radiology exams conducted in the last month",
        "query": "SELECT COUNT(*) as exams_last_month FROM lz_radiology_exams WHERE exam_date >= NOW() - INTERVAL '1 month'",
        "contexts": " | ".join([
            "Table: lz_radiology_exams",
            "Columns: exam_id, patient_id, exam_date, exam_type",
            "Description: This table tracks radiology exams, including exam ID, patient ID, exam date, and type of exam."
        ])
    },
    {
        "input": "List all invoices with their corresponding receipts",
        "query": "SELECT i.invoiceid, i.customerid, i.invoicedate, i.duedate, i.totalamount, r.receiptid, r.paymentamount FROM lz_invoices i LEFT JOIN lz_receipts r ON i.invoiceid = r.invoiceid",
        "contexts": " | ".join([
            "Table: lz_invoices, lz_receipts",
            "Columns: invoice_id, customer_id, invoice_date, due_date, total_amount, receipt_id, payment_amount",
            "Description: The `lz_invoices` table contains invoice data, including customer ID, invoice date, due date, and total amount. The `lz_receipts` table contains payment records linked to invoices."
        ])
    },
    {
        "input": "list of doctors by department",
        "query": "SELECT department_id, doctor_name FROM lz_doctors ORDER BY department_id, doctor_name",
        "contexts": " | ".join([
            "Table: lz_employees",
            "Columns: employee_id, first_name, department_id",
            "Description: This table contains information about doctors, including their ID, name, and department."
        ])
    },
    {
        "input": "Get total amount invoiced and total amount paid for each customer",
        "query": "SELECT i.customerid, SUM(i.totalamount) AS total_amount_invoiced, COALESCE(SUM(r.paymentamount), 0) AS total_amount_paid FROM lz_invoices i LEFT JOIN lz_receipts r ON i.invoiceid = r.invoiceid GROUP BY i.customerid",
        "contexts": " | ".join([
            "Table: lz_invoices, lz_receipts",
            "Columns: invoice_id, customer_id, total_amount, payment_amount",
            "Description: The `lz_invoices` table stores invoice details like customer ID, total amount invoiced. The `lz_receipts` table tracks payments made for these invoices."
        ])
    },
    {
    "input": "list all item costs effective after a certain date",
    "query": "SELECT * FROM lz_item_costs WHERE effective_date > '2024-01-01'",
    "contexts": " | ".join([
        "Table: lz_item_costs",
        "Columns: cost_id, item_id, cost_amount, effective_date",
        "Description: This table contains details of item costs, allowing filtering by effective date."
    ])
}, 
    {
    "input": "get average item cost amount",
    "query": "SELECT AVG(cost_amount) AS average_cost FROM lz_item_costs",
    "contexts": " | ".join([
        "Table: lz_item_costs",
        "Columns: average_cost",
        "Description: This table provides cost information, including the average cost amount across all items."
    ])
},
    {
    "input": "list item costs with effective dates",
    "query": "SELECT item_id, cost_amount, effective_date FROM lz_item_costs",
    "contexts": " | ".join([
        "Table: lz_item_costs",
        "Columns: item_id, cost_amount, effective_date",
        "Description: This table tracks the costs of items, along with their effective dates."
    ])
},
    {
    "input": "list item costs by cost type",
    "query": "SELECT cost_type, COUNT(*) AS cost_count FROM lz_item_costs GROUP BY cost_type",
    "contexts": " | ".join([
        "Table: lz_item_costs",
        "Columns: cost_type, cost_count",
        "Description: This table tracks the different types of costs associated with items, including the count of each cost type."
    ])
},
    {
        "input": "List all receipts along with the corresponding invoice details",
        "query": """
            SELECT r.receipt_id, r.payment_amount, i.invoice_id, i.total_amount as invoice_amount
            FROM lz_receipts r
            JOIN lz_invoices i ON r.invoice_id = i.invoice_id
        """,
        "contexts": " | ".join([
            "Table: lz_receipts, lz_invoices",
            "Columns: receipt_id, payment_amount, invoice_id, total_amount",
            "Description: The `lz_receipts` table records payment details linked to invoices stored in the `lz_invoices` table."
        ])
    },
    {
        "input": "List all nurses along with their department names",
        "query": """
            SELECT n.nurse_id, n.nurse_name, d.department_name
            FROM lz_nurses n
            JOIN lz_departments d ON n.department_id = d.department_id
        """,
        "contexts": " | ".join([
            "Table: lz_nurses, lz_departments",
            "Columns: nurse_id, nurse_name, department_id, department_name",
            "Description: The `lz_nurses` table contains information about nurses, while the `lz_departments` table includes department details."
        ])
    },
    {
        "input": "total revenue by customer",
        "query": "SELECT customerid, SUM(totalamount) AS total_revenue FROM lz_invoices GROUP BY customerid",
        "contexts": " | ".join([
            "Table: lz_invoices",
            "Columns: customer_id, total_amount",
            "Description: This table records invoice data, including customer ID and the total amount billed."
        ])
    },
    {
        "input": "list all the invoices in the second financial quarter of 2024",
        "query": "SELECT * FROM lz_invoices WHERE EXTRACT(QUARTER FROM invoicedate) = 2 AND EXTRACT(YEAR FROM invoicedate) = 2024",
        "contexts": " | ".join([
            "Table: lz_invoices",
            "Columns: invoice_id, invoice_date, total_amount",
            "Description: This table stores invoice details, including invoice ID, date, and total amount, allowing filtering by quarter and year."
        ])
    },
    {
        "input": "Find receipts without corresponding invoices",
        "query": "SELECT r.receiptid, r.invoiceid, r.receiptdate, r.paymentamount, r.paymentmethod, r.paymentreference, r.paymentstatus FROM lz_receipts r LEFT JOIN lz_invoices i ON r.invoiceid = i.invoiceid WHERE i.invoiceid IS NULL",
        "contexts": " | ".join([
            "Table: lz_receipts, lz_invoices",
            "Columns: receipt_id, invoice_id, payment_amount, payment_method, payment_status",
            "Description: The `lz_receipts` table stores payment information, while the `lz_invoices` table contains invoice details, enabling the identification of receipts without matching invoices."
        ])
    },
    {
        "input": "List all employees along with their department names",
        "query": """
            SELECT e.employee_id, e.employee_name, d.department_name
            FROM lz_employees e
            JOIN lz_departments d ON e.department_id = d.department_id
        """,
        "contexts": " | ".join([
            "Table: lz_employees, lz_departments",
            "Columns: employee_id, employee_name, department_id, department_name",
            "Description: The `lz_employees` table contains information about employees, while the `lz_departments` table includes department details."
        ])
    }
]



#Added by Aruna
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
import streamlit as st

@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        Chroma,
        k=1,
        input_keys=["input"],
    )
    return example_selector